""" Discussion views. """

from django.shortcuts import render, get_object_or_404, redirect
from models import Topic, Comment, TopicUser, Group, Profile
from models import Like, Dislike, Notification
from rest_framework import viewsets
from serializers import CommentSerializer, TopicUserSerializer, GroupSerializer
from serializers import NotificationSerializer
from forms import TopicForm, DemographicsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from embedly import Embedly
from settings import EMBEDLY_KEY
from notifications import notify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
embedly_client = Embedly(EMBEDLY_KEY)


def index(request):
    """ List all topics. """
    TOPICS_PER_PAGE = 6

    paginator = Paginator(Topic.objects.all().order_by('-pinned', '-last_post'), TOPICS_PER_PAGE)

    page = request.GET.get('page')

    if request.user.is_authenticated():
        p = request.user.profile
        p.last_interaction = timezone.now()
        p.save()

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        topics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        topics = paginator.page(paginator.num_pages)

    return render(request, "index.html",
                  {"topics": topics,
                   "start_iterator": (topics.number - 1) * TOPICS_PER_PAGE,
                   "paginator": paginator,
                   "total_users": User.objects.all().count(),
                   "active_users": Profile.objects.filter(active=True).count()})


def notifications_read(request):
    """Mark notifications as read."""
    for notification in request.user.notifications.unread():
        notification.read = True
        notification.read_time = datetime.now()
        notification.save()
    return JsonResponse({})


def info(request):
    """Show experiment information."""
    return render(request, "info.html")

# @login_required
def demographics(request):
    """Input demographic information."""
    form = DemographicsForm()
    if request.method == "POST":
        form = DemographicsForm(request.POST)
        if form.is_valid():
            # Create a new participant and record demographics
            return redirect("index")
    return render(request, "demographics.html", {
                  "form": form
                  })


def profile(request, pk):
    """Show a user's post history."""
    user = get_object_or_404(User, pk=pk)

    sort_by = request.GET.get("sort", "recent")

    COMMENTS_PER_PAGE = 10

    comments = Comment.objects.filter(author__user=user)

    if sort_by == 'recent':
        comments = comments.order_by('-created_at')
    else:
        # comments = comments.annotate(num_likes=Count('liked_by'))
        # comments = comments.annotate(num_dislikes=Count('disliked_by'))
        # # comments = comments.annotate(votes=Sum(F('num_likes')+F('num_dislikes')))
        # comments = comments.extra(select={'votes': 'num_likes - num_dislikes'}).extra(order_by=['votes'])
        # comments = comments.order_by('-num_dislikes')

        # TODO: We can do this in sql somehow - for now we do it the slow way
        comments = sorted(comments, key=lambda c : 0 - c.like_count())

    paginator = Paginator(comments, COMMENTS_PER_PAGE)

    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    return render(request, "profile.html",
                  {"comments": comments,
                   "paginator": paginator,
                   "user": user,
                   "sort_by": sort_by})


@login_required
def create_topic(request):
    """ Create a topic. """
    form = TopicForm()
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = request.user

            if 'url' in request.POST:
                t.url = request.POST['url']
                if t.url:
                    o = embedly_client.oembed(t.url)
                    if not o.get("error"):
                        t.embed_html = o.get('html')
                        t.thumbnail_url = o.get('thumbnail_url')
            t.save()
            messages.success(request, "Your topic has been created")
            return redirect("discussion", t.pk)
    return render(request, "create_topic.html", {"form": form})


@login_required
def consent(request):
    """Consent to basic rules."""
    if request.method == "POST":
        p = request.user.profile
        p.given_consent = True
        p.save()
        return redirect(request.GET.get("next", "/"))
    return render(request, "consent.html",
                  {"next": request.GET.get("next", "/")})


@login_required
@require_POST
@csrf_exempt
def communicate(request):
    """Consent to follow up communication."""
    p = request.user.profile
    p.has_seen_contacted = True
    if request.POST['contact'] == 'True':
        p.can_be_contacted = True
    p.save()
    return JsonResponse({})

def discussion(request, pk):
    """ View an individual discussion. """
    topic = get_object_or_404(Topic, pk=pk)
    r = JSONRenderer()
    comments = r.render([CommentSerializer(c).data
                        for c in topic.comments.all()])
    users = r.render([TopicUserSerializer(u).data for u in topic.users.all()])
    groups = r.render([GroupSerializer(g).data for g in topic.groups.all()])

    topic_user = None
    if request.user.is_authenticated():
        topic_user = request.user.topic_user(topic)

    return render(request, "discussion.html",
                  {"topic": topic,
                   "comments": comments,
                   "users": users,
                   "groups": groups,
                   "total_users": User.objects.all().count(),
                   "topic_user": topic_user,
                   "active_users": Profile.objects.filter(active=True).count()}
                  )


@login_required
@require_POST
@csrf_exempt
def lookup_url(request):
    url = request.POST['url']
    o = embedly_client.extract(url)
    if not o.get("error"):
        return JsonResponse({
            "title": o.get("title", ""),
            "content": o.get("description", ""),
            "images": o.get("images", [])
        })
    return JsonResponse({
            "title": "",
            "content": "",
            "images": []
        })


@login_required
def view_group(request, pk, group, sort_by):
    """ The user has clicked on a group. """
    topic = get_object_or_404(Topic, pk=pk)
    topicuser = request.user.topic_user(topic)
    topicuser.log("view group", {"group": group, "sort_by": sort_by})
    return HttpResponse("")


@login_required
@require_POST
def reply(request, pk):
    """ reply to a topic or comment. """
    topic = get_object_or_404(Topic, pk=pk)

    parent = None
    if request.POST.get('parent'):
        parent = get_object_or_404(Comment, pk=request.POST['parent'])

    comment = Comment(text=request.POST['text'],
                      topic=topic,
                      parent=parent,
                      author=request.user.topic_user(topic),
                      created_at=datetime.now())
    comment.save()

    data = {
        "respond_user": comment.author,
        "topic": topic,
        "comment": comment.text
    }

    # TODO: Don't generate a notification if the respond_user is the user

    notify(request, topic.created_by, "topic_reply", data)

    if parent:
        users = set([topic.created_by] + [r.author.user for r in parent.replies.all()])
        for u in users:
            notify(request, u, "comment_reply", data)

    topic.last_post = datetime.now()
    topic.save()
    return redirect("discussion", topic.pk)


@login_required
@require_POST
def like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    topic_user = request.user.topic_user(comment.topic)
    for c in Dislike.objects.filter(user=topic_user, comment=comment):
        c.active = False
        c.save()
    if comment.liked_by.filter(pk=topic_user.pk).count() < 1:
        Like(user=topic_user, comment=comment).save()
    comment.save()
    return HttpResponse("")

@login_required
@require_POST
def dislike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    topic_user = request.user.topic_user(comment.topic)
    for c in Like.objects.filter(user=topic_user, comment=comment):
        c.active = False
        c.save()
    if comment.disliked_by.filter(pk=topic_user.pk).count() < 1:
        Dislike(user=topic_user, comment=comment).save()
    comment.save()
    return HttpResponse("")


@login_required
@staff_member_required
@require_POST
def pin_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.pinned = True
    topic.save()
    return redirect("discussion", topic.pk)


@login_required
@staff_member_required
@require_POST
def unpin_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.pinned = False
    topic.save()
    return redirect("discussion", topic.pk)


class TopicUserViewSet(viewsets.ModelViewSet):

    """API endpoint that allows users to be viewed or edited."""

    serializer_class = TopicUserSerializer

    def get_queryset(self):
        return TopicUser.objects.filter(
            topic__id=self.request.resolver_match.kwargs['pk'])


class CommentViewSet(viewsets.ModelViewSet):

    """API endpoint that allows comments to be viewed or edited."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            topic__id=self.request.resolver_match.kwargs['pk'])


class NotificationViewSet(viewsets.ModelViewSet):

    """API endpoint that allows notifications to be viewed."""
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return []
        return Notification.objects.all().filter(user=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):

    """API endpoint that allows groups to be viewed or edited."""
    serializer_class = GroupSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            p = self.request.user.profile
            p.last_interaction = timezone.now()
            p.save()
            tu = self.request.user.topic_user(
                Topic.objects.get(pk=self.request.resolver_match.kwargs['pk']))
            tu.last_interaction = timezone.now()
            tu.save()
        return Group.objects.filter(
            topic__id=self.request.resolver_match.kwargs['pk'])

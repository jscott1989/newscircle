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
from forms import UsernameForm
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
embedly_client = Embedly(EMBEDLY_KEY)


def index(request):
    """ List all topics. """
    TOPICS_PER_PAGE = 6

    paginator = Paginator(Topic.objects.filter(hidden=False).order_by('-featured', '-pinned', '-last_post'), TOPICS_PER_PAGE)

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


@login_required
def notifications_read(request):
    """Mark notifications as read."""
    for notification in request.user.notifications.unread():
        notification.read = True
        notification.read_time = timezone.now()
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

    comments = Comment.objects.filter(author__user=user, topic__hidden=False)

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


def create_topic(request):
    """ Create a topic. """

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)

            if not request.user.is_authenticated():
                # Record what they posted and then send them to login
                request.session['topic'] = form.cleaned_data
                request.session['topic_include_image'] = request.POST.get("include_image")
                request.session['topic_image'] = request.POST.get("image")
                request.session['login_prefix'] = render_to_string(
                    "login_new_topic.html",
                    form.cleaned_data,
                    context_instance=RequestContext(request))
                return redirect(reverse("account_login") + "?next=/create_topic")

            t.created_by = request.user

            if request.POST.get("include_image"):
                t.description = "![](" + request.POST['image'] + ")\n\n" + t.description
                t.thumbnail_url = request.POST['image']
            t.save()
            messages.success(request, "Your topic has been created")
            return redirect("discussion", t.pk)
    elif 'topic' in request.session and request.user.is_authenticated():
        t = Topic(title=request.session['topic']['title'], description=request.session['topic']['description'], url=request.session['topic']['url'])
        t.created_by = request.user
        if request.session.get("topic_include_image"):
            t.description = "![](" + request.session['topic_image'] + ")\n\n" + t.description
            t.thumbnail_url = request.session['topic_image']
        t.save()
        messages.success(request, "Your topic has been created")
        del request.session['topic']
        return redirect("discussion", t.pk)
    messages.error(request, "There was a problem submitting this link.")
    return redirect("index")


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
def settings(request):
    """Settings."""
    return render(request, "settings.html")


@login_required
def edit_username(request):
    """Change username."""
    form = UsernameForm(initial={"username": request.user.username})
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.save()
            return redirect("settings")
    return render(request, "edit_username.html",
                  {"form": form})


@login_required
def notification_settings(request):
    """Change notification settings."""
    if request.method == "POST":
        p = request.user.profile
        p.notifications_setting = request.POST['notifications']
        p.save()
        messages.success(request, "Your settings have been saved")
        return redirect("settings")
    return render(request, "notification_settings.html")


@login_required
def contact_settings(request):
    """Change contact settings."""
    if request.method == "POST":
        p = request.user.profile
        p.can_be_contacted = request.POST['can_be_contacted'] == "1"
        p.save()
        messages.success(request, "Your settings have been saved")
        return redirect("settings")
    return render(request, "contact_settings.html")


def reply(request, pk):
    """ reply to a topic or comment. """

    def _notify_reply(comment):
        data = {
            "respond_user": comment.author,
            "topic": comment.topic,
            "comment": comment.text
        }

        users = [topic.created_by]
        if comment.parent:
            # Make a list of all users at this level and above
            p = comment.parent
            users += [p.author.user]
            while p.parent:
                p = p.parent
                users.append(p.author.user)

            users += [r.author.user for r in parent.replies.all()]

        for u in set([u for u in users if not comment.author.user == u]):
            notify(request, u, "comment_reply", data)

    topic = get_object_or_404(Topic, pk=pk)

    if request.method == "POST":
        parent = None
        if request.POST.get('parent'):
            parent = get_object_or_404(Comment, pk=request.POST['parent'])
        if not request.user.is_authenticated():
            # Record what they posted and then send them to login
            request.session['comment'] = {
                "text": request.POST['text'],
                "topic_pk": topic.pk,
            }

            if parent:
                request.session["comment"]["parent_pk"] = parent.pk
                
            request.session['login_prefix'] = render_to_string(
                "login_reply.html",
                context_instance=RequestContext(request))
            return redirect(reverse("account_login") + "?next=/discussion/" + str(topic.pk) + "/reply")

        comment = Comment(text=request.POST['text'],
                          topic=topic,
                          parent=parent,
                          author=request.user.topic_user(topic),
                          created_at=timezone.now())
        comment.save()

        _notify_reply(comment)

        topic.last_post = timezone.now()
        topic.save()
        return JsonResponse({})
    elif request.user.is_authenticated() and "comment" in request.session:
        parent = None
        if "parent_pk" in request.session["comment"]:
            parent = get_object_or_404(Comment, pk=request.session["comment"]["parent_pk"])
        comment = Comment(text=request.session["comment"]["text"],
                          topic=topic,
                          parent=parent,
                          author=request.user.topic_user(topic),
                          created_at=timezone.now())
        comment.save()

        _notify_reply(comment)

        topic.last_post = timezone.now()
        topic.save()
        del request.session["comment"]
        messages.success(request, "Your comment has been posted")
        return redirect("discussion", pk)

    messages.error(request, "There was a problem posting that comment")
    return redirect("discussion", pk)


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

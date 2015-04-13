""" Discussion views. """

from django.shortcuts import render, get_object_or_404, redirect
from models import Topic, Comment, TopicUser, Group
from rest_framework import viewsets
from serializers import CommentSerializer, TopicUserSerializer, GroupSerializer
from forms import TopicForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import datetime


def index(request):
    """ List all topics. """
    return render(request, "index.html", {"topics": Topic.objects.all()})


@login_required
def create_topic(request):
    """ Create a topic. """
    form = TopicForm()
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your topic have been created")
            return redirect("index")
    return render(request, "create_topic.html", {"form": form})


def discussion(request, pk):
    """ View an individual discussion. """
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "discussion.html", {"topic": topic})


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


class GroupViewSet(viewsets.ModelViewSet):

    """API endpoint that allows groups to be viewed or edited."""
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(
            topic__id=self.request.resolver_match.kwargs['pk'])

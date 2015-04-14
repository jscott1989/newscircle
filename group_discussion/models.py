""" Discussion models. """

from django.db import models
from django.contrib.auth.models import User
import hashlib


class Topic(models.Model):

    """ A topic of discussion. """

    title = models.CharField(max_length=255)
    description = models.TextField()
    locked = models.BooleanField(default=False)

    def __unicode__(self):
        """ Return the title of the topic. """
        return self.title


class Group(models.Model):

    """ A group which exists within a topic. """

    topic = models.ForeignKey(Topic, related_name="groups")
    number = models.IntegerField()


class TopicUser(models.Model):

    """ An instance of a user used for a specific topic. """

    user = models.ForeignKey("auth.User", related_name="topic_users")
    topic = models.ForeignKey(Topic, related_name="users")
    group = models.ForeignKey(Group, null=True, related_name="users",
                              on_delete=models.SET_NULL)

    @property
    def username(self):
        """ The user's username. """
        return self.user.username

    @property
    def avatar_url(self):
        m = hashlib.md5()
        m.update(self.user.username)
        return "http://www.gravatar.com/avatar/%s?d=retro&s=500" % m.hexdigest()
    


def get_topic_user(user, topic):
    """ Get the TopicUser for a given user and topic. """
    return user.topic_users.get_or_create(topic=topic)[0]
User.topic_user = get_topic_user


class Comment(models.Model):

    """ A comment by a user. """

    created_at = models.DateTimeField()
    text = models.TextField()
    topic = models.ForeignKey(Topic, related_name="comments")
    parent = models.ForeignKey("Comment", null=True, related_name="replies")
    author = models.ForeignKey(TopicUser, related_name="comments")
    liked_by = models.ManyToManyField(TopicUser, related_name="likes")
    disliked_by = models.ManyToManyField(TopicUser, related_name="dislikes")

    def __unicode__(self):
        """ Return the author and content of the comment. """
        return "<%s> %s" % (self.author.username, self.text)

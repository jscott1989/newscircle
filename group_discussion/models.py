""" Discussion models. """

from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):

    """ A topic of discussion. """

    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        """ Return the title of the topic. """
        return self.title


class TopicUser(models.Model):

    """ An instance of a user used for a specific topic. """

    user = models.ForeignKey("auth.User", related_name="topic_users")
    topic = models.ForeignKey(Topic)

    @property
    def username(self):
        """ The user's username. """
        return self.user.username

def get_topic_user(user, topic):
    return user.topic_users.get_or_create(topic=topic)[0]
User.topic_user = get_topic_user

class Comment(models.Model):

    """ A comment by a user. """

    text = models.TextField()
    topic = models.ForeignKey(Topic, related_name="comments")
    parent = models.ForeignKey("Comment", null=True, related_name="replies")
    author = models.ForeignKey(TopicUser, related_name="comments")
    liked_by = models.ManyToManyField("auth.User", related_name="likes")
    disliked_by = models.ManyToManyField("auth.User", related_name="dislikes")

    def __unicode__(self):
        """ Return the author and content of the comment. """
        return "<%s> %s" % (self.author.username, self.text)

""" Discussion models. """

from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):

    """ A topic of discussion. """

    title = models.CharField(max_length=255)
    description = models.TextField()
    locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        """ Return the title of the topic. """
        return self.title

    @property
    def root_comments(self):
        """ Return all root comments. """
        return [c for c in self.comments if not self.parent]

    @property
    def created_time_ago(self):
        """TODO:Return the time ago this was created."""
        return "1 hour ago"


class Group(models.Model):

    """ A group which exists within a topic. """

    topic = models.ForeignKey(Topic, related_name="groups")
    number = models.IntegerField()

    @property
    def comments(self):
        """ Return comment IDs created by members of this group. """
        return sum([[c.id for c in u.comments.all()] for u in self.users.all()], [])

    @property
    def root_comments(self):
        """ Return comment IDs created by members of this group with no parent. """
        return sum([[c.id for c in u.comments.filter(parent=None)] for u in self.users.all()], [])

    @property
    def representative_comment(self):
        comments = sum([[c for c in u.comments.all()] for u in self.users.all()], [])

        if len(comments) == 0:
            return None

        only_root_comments = [c for c in comments if not c.parent]

        if len(only_root_comments) == 0:
            return None
            # comments = sorted(comments, key=lambda c : c.group_like_count(), reverse=True)
            # return comments[0].id
        only_root_comments = sorted(only_root_comments,
                                    key=lambda c : c.group_like_count(), reverse=True)
        return only_root_comments[0].id


    


class TopicUser(models.Model):

    """ An instance of a user used for a specific topic. """

    user = models.ForeignKey("auth.User", related_name="topic_users")
    topic = models.ForeignKey(Topic, related_name="users")
    group = models.ForeignKey(Group, null=True, related_name="users",
                              on_delete=models.SET_NULL)
    # This represents the number of in-group links per out-group link
    group_centrality = models.IntegerField(null=True)

    @property
    def username(self):
        """ The user's username. """
        return self.user.username

    @property
    def avatar_url(self):
        # TODO: Stop hotlinking - pull these avatars
        return "https://disqus.com/api/users/avatars/%s.jpg" % self.username


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

    def group_like_count(self):
        return len(self.group_liked_by()) - len(self.group_disliked_by())
    
    def group_liked_by(self):
        return [u.id for u in self.liked_by.all() if u.group == self.author.group]

    def group_disliked_by(self):
        return [u.id for u in self.disliked_by.all() if u.group == self.author.group]

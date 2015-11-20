""" Discussion models. """

from django.db import models
from django.contrib.auth.models import User
from utils import pretty_date
import re
import json
import urlparse

# Ensure that every user has an associated profile
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Profile(models.Model):

    """Member Profile."""

    user = models.OneToOneField(User, related_name="existing_profile")
    last_interaction = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    given_consent = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)
    has_seen_contacted = models.BooleanField(default=False)


class Topic(models.Model):

    """ A topic of discussion. """

    title = models.CharField(max_length=255)
    description = models.TextField()
    locked = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    last_post = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    url = models.URLField(null=True)
    embed_html = models.TextField(null=True)

    def __unicode__(self):
        """ Return the title of the topic. """
        return self.title

    @property
    def domain(self):
        if not self.url:
            return ""
        return urlparse.urlparse(self.url).netloc

    @property
    def logo(self):
        m = {
            "youtube": "youtube.png",
            "theguardian": "guardian.png",
            "dailymail": "dailymail.png",
            "mirror.co.uk": "dailymirror.png",
            "express.co.uk": "express.png",
            "facebook": "facebook.png",
            "telegraph.co.uk": "telegraph.png",
            "twitter": "twitter.png"
        }
        domain = self.domain
        for k, v in m.items():
            if k in domain:
                return '<img class="source" src="/static/img/sources/' + v + '">'
        return '(' + domain + ')'
    
    

    @property
    def root_comments(self):
        """ Return all root comments. """
        return [c for c in self.comments if not self.parent]

    @property
    def created_time_ago(self):
        """Return the time ago this was created."""
        return pretty_date(self.created_at)


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

    @property
    def most_central_user(self):
        # TODO: Some calculation to decide most central
        v = sorted(self.users.all(), key = lambda u : u.group_centrality, reverse=True)
        if len(v) == 0:
            return None
        return v[0]
    


class TopicUser(models.Model):

    """ An instance of a user used for a specific topic. """

    user = models.ForeignKey("auth.User", related_name="topic_users")
    topic = models.ForeignKey(Topic, related_name="users")
    group = models.ForeignKey(Group, null=True, related_name="users",
                              on_delete=models.SET_NULL)
    # This represents the number of in-group links per out-group link
    group_centrality = models.IntegerField(null=True)

    last_interaction = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


    def log(self, action, details=None):
        if not details:
            details = {}
        log = Log(user=self, action=action, details=json.dumps(details))
        log.save()

    @property
    def username(self):
        """ The user's username. """
        return self.user.username

    @property
    def avatar_url(self):
        # TODO: Stop hotlinking - pull these avatars
        return "https://disqus.com/api/users/avatars/%s.jpg" % self.username

    @property
    def karma(self):
        return sum([x.liked_by.count() - x.disliked_by.count() for x in self.comments.all()])

    @property
    def group_karma(self):
        return sum([len(x.group_liked_by()) - len(x.group_disliked_by()) for x in self.comments.all()])

    @property
    def user_pk(self):
        return self.user.pk
    


def get_topic_user(user, topic):
    """ Get the TopicUser for a given user and topic. """
    return user.topic_users.get_or_create(topic=topic)[0]
User.topic_user = get_topic_user


def get_total_karma(user):
    return sum([topicuser.karma for topicuser in user.topic_users.all()])

User.total_karma = property(get_total_karma)


def get_group_karma(user):
    return sum([topicuser.group_karma for topicuser in user.topic_users.all()])

User.group_karma = property(get_group_karma)


class Comment(models.Model):

    """ A comment by a user. """

    created_at = models.DateTimeField()
    text = models.TextField()
    topic = models.ForeignKey(Topic, related_name="comments")
    parent = models.ForeignKey("Comment", null=True, related_name="replies")
    author = models.ForeignKey(TopicUser, related_name="comments")
    liked_by_raw = models.ManyToManyField(TopicUser, related_name="likes",
                                      through="Like")
    disliked_by_raw = models.ManyToManyField(TopicUser, related_name="dislikes",
                                         through="Dislike")
    embed_html = models.TextField(null=True)

    @property
    def liked_by(self):
        return self.liked_by_raw.filter(like__active=True)

    @property
    def disliked_by(self):
        return self.disliked_by_raw.filter(dislike__active=True)


    def save(self, *args, **kwargs):
        if not self.embed_html:
            # Calculate embed
            # First we match for any URLS
            m = re.findall("(?P<url>https?://[^\s]+)", self.text)
            for url in m:
                # Now pull out the html from embedly
                o = embedly_client.oembed(url)
                if not o.get("error") and o.get("html"):
                    self.embed_html = o['html']
                    break
        super(Comment, self).save(*args, **kwargs)

    def __unicode__(self):
        """ Return the author and content of the comment. """
        return "<%s> %s" % (self.author.username, self.text)

    def like_count(self):
        return self.liked_by.count() - self.disliked_by.count()

    def group_like_count(self):
        return len(self.group_liked_by()) - len(self.group_disliked_by())
    
    def group_liked_by(self):
        return [u.id for u in self.liked_by.all() if u.group and u.group == self.author.group]

    def group_disliked_by(self):
        return [u.id for u in self.disliked_by.all() if u.group and u.group == self.author.group]

    @property
    def created_time_ago(self):
        """Return the time ago this was created."""
        return pretty_date(self.created_at)


class Like(models.Model):
    """A like."""
    user = models.ForeignKey(TopicUser)
    comment = models.ForeignKey(Comment)
    time_voted = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Dislike(models.Model):
    """A dislike."""
    user = models.ForeignKey(TopicUser)
    comment = models.ForeignKey(Comment)
    time_voted = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Log(models.Model):
    """An action performed by a user."""
    user = models.ForeignKey(TopicUser, related_name="logs")
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    details = models.TextField()

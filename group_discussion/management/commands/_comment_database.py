from pony.orm import Database, Required, PrimaryKey, Set, Optional
from datetime import datetime
import os
import urlparse
from pony.orm import TransactionError
import itertools
import hashlib

GROUPING = 0
DATABASE_URL = "postgres://comments:comments@127.0.0.1/comments"

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(DATABASE_URL)

db = Database('postgres', user=url.username, password=url.password,
              host=url.hostname, database=url.path[1:])


class Story(db.Entity):
    url = PrimaryKey(unicode, 1024)
    site = Required(unicode)
    summary = Optional(unicode)
    title = Required(unicode, 1024)
    disqus_thread = Required("DisqusThread")
    top_stories = Set("TopStory")


class DisqusThread(db.Entity):
    disqus_shortname = Required(unicode)
    thread_id = Required(unicode)
    PrimaryKey(disqus_shortname, thread_id)
    comments = Set("Comment")
    groups = Set("Group")
    stories = Set("Story")


class TopStory(db.Entity):
    date = Required(datetime)
    site = Required(unicode)
    rank = Required(int)
    story = Required(Story)
    PrimaryKey(site, date, rank)


class Person(db.Entity):
    id = PrimaryKey(unicode)
    name = Required(unicode, 10240)
    likes = Set("Comment", reverse="liked_by")
    dislikes = Set("Comment", reverse="disliked_by")
    posted = Set("Comment", reverse="author")
    about = Optional(unicode, 10240)
    joined_at = Optional(datetime)
    reputation = Optional(unicode)
    location = Optional(unicode, 10240)
    groups = Set("Group")

    @property
    def avatar_url(self):
        m = hashlib.md5()
        m.update(self.name)
        return "http://www.gravatar.com/avatar/%s?d=retro&s=500" % m.hexdigest()

    def get_group_for_thread(self, thread, grouping_id=0):
        for i in self.groups:
            if i.disqus_thread == thread and i.grouping.id == grouping_id:
                return i


class Comment(db.Entity):
    id = PrimaryKey(unicode)
    disqus_thread = Required(DisqusThread)
    created_at = Required(datetime)
    author = Required(Person, reverse="posted")
    liked_by = Set("Person", reverse="likes")
    likes = Required(int)
    disliked_by = Set("Person", reverse="dislikes")
    dislikes = Required(int)
    message = Required(unicode, 1024000)
    parent_id = Optional(unicode)
    parent = Optional("Comment", reverse="responses")
    responses = Set("Comment", reverse="parent")
    is_spam = Optional(bool)
    reports = Optional(int)
    approved = Optional(bool)
    sentiment = Optional(int)

    def replies(self):
        """ Return replies ordered by posted date. """
        return sorted(self.responses, key=lambda p: p.created_at)

    def replies_ordered_by_overall_votes(self):
        """ Return replies ordered by votes. """
        return sorted(self.responses, key=lambda p: len(p.liked_by) - len(p.disliked_by), reverse=True)

    def replies_by_group(self, group):
        """ Return all the replies to this comment which come from a given group. Ordered by in-group votes. """
        valid_replies = [r for r in self.responses if r.author.get_group_for_thread(self.disqus_thread) == group]
        return sorted(valid_replies, key=lambda p: p.group_likes() - p.group_dislikes())

    def group_likes(self):
        """ Return the number of likes from within this group. """
        our_group = self.author.get_group_for_thread(self.disqus_thread)
        return len([u for u in self.liked_by if
                    u.get_group_for_thread(self.disqus_thread) == our_group])

    def group_dislikes(self):
        """ Return the number of dislikes from within this group. """
        our_group = self.author.get_group_for_thread(self.disqus_thread)
        return len([u for u in self.disliked_by if
                    u.get_group_for_thread(self.disqus_thread) == our_group])


class Grouping(db.Entity):
    # This is a set of groups - so one user may be in several groups
    # depending on the grouping strategy
    name = Required(unicode)
    groups = Set("Group")


class Group(db.Entity):
    disqus_thread = Required(DisqusThread)
    grouping = Required(Grouping)
    name = Required(unicode)
    people = Set("Person")
    PrimaryKey(disqus_thread, grouping, name)

    @property
    def name_formatted(self):
        return "Group " + str(self.id + 1)

    @property
    def id(self):
        return int(self.name.split(" ")[1])

    def representative_comment(self):
        """ Get the highest rated comment from that group (as rating by members of the group) """
        p = self.root_posts
        if len(p) == 0:
            return None
        return p[0]

    @property
    def root_posts(self):
        """ Get the root comments ordered by votes. """
        all_posts = itertools.chain(*[[c for c in p.posted if c.disqus_thread == self.disqus_thread and not c.parent] for p in self.people])

        def filtered_likes(c):
            return len([p for p in c.liked_by if p.get_group_for_thread(self.disqus_thread) == self])

        def filtered_dislikes(c):
            return len([p for p in c.disliked_by if p.get_group_for_thread(self.disqus_thread) == self])

        all_posts = sorted(all_posts, key = lambda c : filtered_likes(c) - filtered_dislikes(c), reverse=True)

        return all_posts

    @property
    def all_posts(self):
        """ Get all posts ordered by votes. """
        all_posts = itertools.chain(*[[c for c in p.posted if c.disqus_thread == self.disqus_thread] for p in self.people])

        def filtered_likes(c):
            return len([p for p in c.liked_by if p.get_group_for_thread(self.disqus_thread) == self])

        def filtered_dislikes(c):
            return len([p for p in c.disliked_by if p.get_group_for_thread(self.disqus_thread) == self])

        all_posts = sorted(all_posts, key = lambda c : filtered_likes(c) - filtered_dislikes(c), reverse=True)

        return all_posts

try:
    db.generate_mapping(create_tables=True)
except TransactionError:
    pass

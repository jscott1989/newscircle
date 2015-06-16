"""Import a discussion from the old research database."""
from django.core.management.base import BaseCommand, CommandError
from _comment_database import Story
from group_discussion.models import Topic, Comment
from pony.orm import db_session
from django.contrib.auth.models import User


class Command(BaseCommand):

    """Import a discussion from the old research database."""

    help = 'Import a discussion from the old research database'

    def add_arguments(self, parser):
        """Import a discussion from the old research database."""
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        """Import a discussion from the old research database."""
        url = args[0]
        with db_session():
            story = Story[url]
            if not story:
                raise CommandError('Story "%s" does not exist' % url)

            # First create the topic
            title = "%s (%s)" % (story.title, story.site)
            topic = Topic.objects.get_or_create(title=title)[0]

            topic.locked = True
            topic.save()

            def get_user(topic, name):
                # First we need to see if there is a real user
                try:
                    user = User.objects.get(username=name)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username=name, email='%s@example.com' % name,
                        password='password')
                return user.topic_user(topic)

            # Delete existing posts
            for comment in topic.comments.all():
                comment.delete()

            # Delete existing users
            for user in topic.users.all():
                user.delete()

            # Delete existing groups
            for group in topic.groups.all():
                group.delete()

            # Load in each post
            comments = {}
            for comment in story.disqus_thread.comments:
                # Get the author
                author = get_user(topic, comment.author.name)

                new_comment = Comment(
                    text=comment.message,
                    topic=topic,
                    author=author,
                    created_at=comment.created_at
                )

                comments[comment.id] = new_comment

                new_comment.save()

                # Load the likes and dislikes
                for liker in comment.liked_by:
                    new_comment.liked_by.add(get_user(topic, liker.name))

                for disliker in comment.disliked_by:
                    new_comment.disliked_by.add(get_user(topic, disliker.name))


            # Ensure posts are linked to their parents
            for comment in story.disqus_thread.comments:
                if comment.parent is not None:
                    comments[comment.id].parent = comments[comment.parent.id]
                    comments[comment.id].save()

            self.stdout.write('Successfully imported "%s"' % url)

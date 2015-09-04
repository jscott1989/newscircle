"""Check if a user has been inactive for more than 60 seconds, if so add inactivity to their log."""
from django.core.management.base import BaseCommand, CommandError
from group_discussion.models import Topic, Group, TopicUser
from networkx import Graph
import community as community_finder
import itertools
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User


class Command(BaseCommand):

    """Check if a user has been inactive for more than 60 seconds, if so add inactivity to their log."""

    help = """Check if a user has been inactive for more than 60 seconds, if so add inactivity to their log."""

    def handle(self, *args, **options):
        """Check if a user has been inactive for more than 60 seconds, if so add inactivity to their log."""

        while True:
            CUTOFF = timezone.now() - timedelta(minutes=1)

            for user in User.objects.all():
                p = user.profile
                if p.last_interaction < CUTOFF and p.active:
                    # Make them inactive
                    p.active = False
                    p.save()
                elif p.last_interaction >= CUTOFF and not p.active:
                    # Make them active
                    p.active = True
                    p.save()

                for topicuser in user.topic_users.all():
                    if topicuser.last_interaction < CUTOFF and topicuser.active:
                        topicuser.active = False
                        topicuser.save()

                        topicuser.log("inactive")

                    elif topicuser.last_interaction >= CUTOFF and not topicuser.active:
                        topicuser.active = True
                        topicuser.save()

                        topicuser.log("active")

            self.stdout.write('Finished checking inactivity')

            import time
            time.sleep(20)
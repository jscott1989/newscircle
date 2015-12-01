"""Send immediate notifications."""
from django.core.management.base import BaseCommand, CommandError
from group_discussion.models import Topic, Group, TopicUser
from django.contrib.auth.models import User
from networkx import Graph
import community as community_finder
import itertools
import random
from django.db import transaction
from group_discussion.models import EMAIL_IMMEDIATELY, DAILY_SUMMARY, WEEKLY_SUMMARY


class Command(BaseCommand):

    """Send immediate notifications."""

    help = 'Send notifications.'

    def handle(self, *args, **options):
        """Send notifications."""
        for user in User.objects.all():
            if user.profile.notifications_setting == WEEKLY_SUMMARY:
                user.email_notifications()

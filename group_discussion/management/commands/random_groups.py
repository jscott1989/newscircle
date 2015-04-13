"""Assign random groups to all users."""
from django.core.management.base import BaseCommand
from group_discussion.models import Topic, Group
import random


class Command(BaseCommand):

    """Assign random groups to all users."""

    help = 'Assign random groups to all users'

    def handle(self, *args, **options):
        """Assign random groups to all users."""
        for topic in Topic.objects.all():
            number_of_groups = random.randint(0, 20)
            for user in topic.users.all():
                user.group = Group.objects.get_or_create(topic=topic, number=random.randint(0, number_of_groups))[0]
                user.save()

        # Delete any empty groups
        for group in Group.objects.all():
            if group.users.count() == 0:
                group.delete()

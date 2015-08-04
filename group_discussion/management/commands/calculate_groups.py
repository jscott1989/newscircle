"""Calculate groups for all topics."""
from django.core.management.base import BaseCommand, CommandError
from group_discussion.models import Topic, Group, TopicUser
from networkx import Graph
import community as community_finder
import itertools

# TODO: Don't calculate for locked topics (nothing will have changed)


def change_relationship(users, user1_id, user2_id, change):
    if user1_id > user2_id:
        user1_id, user2_id = user2_id, user1_id
    if not user1_id in users:
        users[user1_id] = {}
    if not user2_id in users[user1_id]:
        users[user1_id][user2_id] = 0
    users[user1_id][user2_id] += change


class Command(BaseCommand):

    """Calculate groups for all topics."""

    help = 'Calculate groups for all topics.'

    def handle(self, *args, **options):
        """Calculate groups for all topics."""
        for topic in Topic.objects.all():

            # Remove existing groups
            for group in topic.groups.all():
                # TODO: Record most central - then later on
                # we can ensure that this person remains in their group
                # - this should ensure some consistency of colour
                group.delete()

            users = {}
            for comment in topic.comments.all():
                # Everyone who liked this plus the author get put into a set
                likers = set([liker.id for liker in comment.liked_by.all()] + [comment.author.id])

                # Dislikers in another set
                dislikers = set([disliker.id for disliker in comment.disliked_by.all()])

                # Users who like the same thing get increased relationship
                for usera, userb in [b for b in itertools.permutations(likers, 2) if b[0] < b[1]]:
                    change_relationship(users, usera, userb, 1)

                # Users who dislike the same thing get increased relationship
                for usera, userb in [b for b in itertools.permutations(dislikers, 2) if b[0] < b[1]]:
                    change_relationship(users, usera, userb, 1)

                # Users who like/dislike the opposite thing get decreased relationship
                for usera, userb in itertools.product(likers, dislikers):
                    change_relationship(users, usera, userb, -1)

            def get_group_centrality(user_id, user_ids):
                in_likes = 0
                out_likes = 0

                for u, v in users.get(user_id, {}).items():
                    if u in user_ids:
                        in_likes += v
                    else:
                        out_likes += v

                return in_likes - out_likes
            
            g = Graph()

            for user, relationships in users.items():
                if user:
                    g.add_node(user)
                    for r, weight in relationships.items():
                        if r:
                            if weight >= 0:
                                # Ignore negative weights
                                g.add_edge(user, r, weight=weight)

            if g.number_of_nodes() == 0 or g.number_of_edges() == 0:
                continue
            communities = {}

            partition = community_finder.best_partition(g)
            for user_id, community_id in partition.items():
                if community_id not in communities:
                    communities[community_id] = []
                communities[community_id].append(user_id)

            # Flatten community ID's (remove communities with only 1 member)
            communities = [c for c in communities.values() if len(c) > 1]
            communities = sorted(communities, key=lambda c: len(c),
                                 reverse=True)

            # Limit to 7 groups, everyone else goes into "other"
            communities = communities[:7]

            for community_id, user_ids in enumerate(communities, 1):
                if len(user_ids) > 1:
                    community = Group(topic=topic, number=community_id)
                    community.save()
                    for user_id in user_ids:
                        t = TopicUser.objects.get(pk=user_id)
                        t.group = community
                        t.group_centrality = get_group_centrality(user_id,
                                                                  user_ids)
                        t.save()
                        t.log("change group", community_id)

            ungrouped_users = TopicUser.objects.filter(group=None, topic=topic)
            for t in ungrouped_users:
                t.log("remove group")

            self.stdout.write('Finished calculating')

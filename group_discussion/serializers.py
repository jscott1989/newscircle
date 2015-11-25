from models import Comment, TopicUser, Group, Notification
from rest_framework import serializers


class TopicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicUser
        fields = ('id', 'username', 'group', 'group_centrality', 'avatar_url', 'user_pk')


class CommentSerializer(serializers.ModelSerializer):

    liked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    disliked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'text', 'author', 'liked_by',
                  'disliked_by', 'replies', 'created_at')
                  # 'group_liked_by', 'group_disliked_by')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'topic', 'number', 'users', 'comments', 'root_comments', 'representative_comment')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'created_time', 'image', 'html', 'read')

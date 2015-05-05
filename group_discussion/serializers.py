from models import Comment, TopicUser, Group
from rest_framework import serializers


class TopicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicUser
        fields = ('id', 'username', 'group', 'group_centrality', 'avatar_url')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'parent', 'text', 'author', 'liked_by',
                  'disliked_by', 'replies', 'created_at')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'topic', 'number', 'users', 'comments', 'root_comments', 'representative_comment')

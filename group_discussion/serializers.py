from models import Comment, TopicUser
from rest_framework import serializers


class TopicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicUser
        fields = ('id', 'username',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'topic', 'parent', 'text', 'author', 'liked_by', 'disliked_by', 'replies')

""" Discussion forms. """

from django import forms
from models import Topic


class TopicForm(forms.ModelForm):

    """ Form for creating a topic. """

    class Meta:
        model = Topic
        fields = ['title', 'description']

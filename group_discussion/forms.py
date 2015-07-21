""" Discussion forms. """

from django import forms
from models import Topic


class TopicForm(forms.ModelForm):

    """ Form for creating a topic. """

    class Meta:
        model = Topic
        fields = ['title', 'description']

    description = forms.CharField(widget=forms.Textarea(attrs={"class":"edit_markdown"}))


class DemographicsForm(forms.Form):

    """Demographics Form."""

    age = forms.ChoiceField(
        choices=(
            ('0', '----',),
            ('14', 'Under 15 years old',),
            ('15', '15-24',),
            ('25', '25-34',),
            ('35', '35-44',),
            ('45', '45-54',),
            ('55', '55-64',),
            ('65', '65+',),
            ('100', 'Prefer not to say',),
        ), label="What is your age?")
    education = forms.ChoiceField(
        choices=(
            ('0', '----',),
            ('1', 'Secondary education - graduated without formal examination qualifications',),
            ('2', 'Secondary education - graduated at ordinary or lower examination level',),
            ('3', 'Secondary education - graduated at advanced or higher examination level',),
            ('4', 'Uncompleted further education College or University',),
            ('5', 'Graduate of any further education College or University',),
            ('6', 'Masters',),
            ('7', 'Doctorate',),
            ('8', 'Post Doctorate',),
            ('9', 'Prefer not to say',),
        ), label="What was your highest level when you finished your education?")
    occupation = forms.ChoiceField(
        choices=(
            ('0', '----',),
            ('1', 'Employed for wages',),
            ('2', 'Self-employed',),
            ('3', 'Out of work and looking for work',),
            ('4', 'Out of work but not currently looking for work',),
            ('5', 'A homemaker',),
            ('6', 'A student',),
            ('7', 'Military',),
            ('8', 'Retired',),
            ('9', 'Unable to work',),
            ('10', 'Prefer not to say',),
        ), label="What is your employment status?")
    gender = forms.ChoiceField(
        choices=(
            ('0', '----',),
            ('1', 'Male',),
            ('2', 'Female',),
            ('3', 'Other',),
            ('4', 'Prefer not to say',),
        ), label="What is your gender?")

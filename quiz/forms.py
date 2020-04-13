from django import forms
from .models import *


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title',)


# class QuestionForm(forms.ModelForm):


class QuestionForm(forms.Form):
    question = forms.CharField(required=True)
    answer1 = forms.CharField(required=True)
    answer2 = forms.CharField(required=True)
    answer3 = forms.CharField(required=False)
    answer4 = forms.CharField(required=False)


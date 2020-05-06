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
    is_correct1 = forms.BooleanField(required=False)
    is_correct2 = forms.BooleanField(required=False)
    is_correct3 = forms.BooleanField(required=False)
    is_correct4 = forms.BooleanField(required=False)

    def is_valid(self):
        valid = super(QuestionForm, self).is_valid()

        if not valid:
            return valid

        if not self.cleaned_data['answer3'] and self.cleaned_data['answer4']:
            self._errors['wrong_order'] = 'Can\'t add 4th answer if 3rd is blank'
            return False
        
        if not self.cleaned_data['is_correct1'] and not self.cleaned_data['is_correct2'] and not self.cleaned_data['is_correct3'] and not self.cleaned_data['is_correct4']:
            self._errors['no_correct_answer'] = 'Specify at least one correct answer'
            return False

        return True

class EditForm(forms.Form):
    question = forms.CharField(required=False)
    answer1 = forms.CharField(required=False)
    answer2 = forms.CharField(required=False)
    answer3 = forms.CharField(required=False)
    answer4 = forms.CharField(required=False)
    is_correct1 = forms.BooleanField(required=False)
    is_correct2 = forms.BooleanField(required=False)
    is_correct3 = forms.BooleanField(required=False)
    is_correct4 = forms.BooleanField(required=False)


class UserAnswerForm(forms.Form):
    is_correct1 = forms.BooleanField(required=False)
    is_correct2 = forms.BooleanField(required=False)
    is_correct3 = forms.BooleanField(required=False)
    is_correct4 = forms.BooleanField(required=False)

class AttemptForm(forms.Form):
    new_attempt = forms.BooleanField(required=True)
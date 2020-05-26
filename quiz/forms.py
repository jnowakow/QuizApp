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

        answers = set()
        ans = 'answer'
        for i in range(1, 5):
            if self.cleaned_data[ans + str(i)]:
                answers.add(i)

        correct_answers = set()
        is_corr = 'is_correct'
        for i in range(1, 5):
            if self.cleaned_data[is_corr + str(i)]:
                correct_answers.add(i)

        if not correct_answers:
            self.errors['no_correct_answer'] = 'Specify at least one correct answer'
            return False

        if correct_answers - answers:
            self.errors['no_correct_answer'] = 'Correct answer should be specified'
            return False

        return True


class EditForm(forms.Form):
    delete_question = forms.BooleanField(required=False)
    question = forms.CharField(required=False)
    answer1 = forms.CharField(required=False)
    answer2 = forms.CharField(required=False)
    answer3 = forms.CharField(required=False)
    answer4 = forms.CharField(required=False)
    is_correct1 = forms.BooleanField(required=False)
    is_correct2 = forms.BooleanField(required=False)
    is_correct3 = forms.BooleanField(required=False)
    is_correct4 = forms.BooleanField(required=False)
    delete_answer_1 = forms.BooleanField(required=False)
    delete_answer_2 = forms.BooleanField(required=False)
    delete_answer_3 = forms.BooleanField(required=False)
    delete_answer_4 = forms.BooleanField(required=False)

    def is_valid(self):
        valid = super(EditForm, self).is_valid()

        if not valid:
            return False

        if self.cleaned_data['delete_question']:
            return True

        if not self.cleaned_data['question']:
            self.errors['question_err'] = 'Specify a question'
            return False

        answers = set()
        ans = 'answer'
        for i in range(1, 5):
            if self.cleaned_data[ans + str(i)]:
                answers.add(i)

        if len(answers) < 2:
            self.errors['answers_num'] = 'There should be at least two answers'
            return False

        correct_answers = set()
        is_corr = 'is_correct'
        for i in range(1, 5):
            if self.cleaned_data[is_corr + str(i)]:
                correct_answers.add(i)

        to_delete = set()
        to_del = 'delete_answer_'
        for i in range(1, 5):
            if self.cleaned_data[to_del + str(i)]:
                to_delete.add(i)

        if not correct_answers - to_delete:
            self.errors['no_correct_answer'] = 'Specify at least one correct answer'
            return False

        if to_delete - answers:
            self.errors['deletion_err'] = 'You cannot delete a question not specified'
            return False

        if len(answers - to_delete) < 2:
            self.errors['answers_num'] = 'There should be at least two answers after deletions'
            return False

        if correct_answers - (answers - to_delete):
            self.errors['no_correct_answer'] = 'Specify at least one correct answer'
            return False

        return True


class UserAnswerForm(forms.Form):
    is_correct1 = forms.BooleanField(required=False)
    is_correct2 = forms.BooleanField(required=False)
    is_correct3 = forms.BooleanField(required=False)
    is_correct4 = forms.BooleanField(required=False)


class AnswerForm(forms.Form):
    def __init__(self, data, question):
        super().__init__(data)
        field_name = "question_%d" % question.pk
        choices = []
        for answer in question.answer_set().all():
            choices.append((answer.pk, answer.answer,))
        field = forms.ChoiceField(label=question.question, required=True,
                                  choices=choices, widget=forms.RadioSelect)


class QuizAnswerForm(forms.Form):
    answers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, data, question):
        super().__init__(data)
        self.question = question.question
        answers = question.answer_set.all()
        self.fields['answers'].choices = [(i, a.answer) for i, a in enumerate(answers)]

        for pos, answer in enumerate(answers):
            if answer.is_correct:
                self.correct = pos
            break


class AttemptForm(forms.Form):
    new_attempt = forms.BooleanField(required=True)

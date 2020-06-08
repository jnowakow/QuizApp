from django import forms
from .models import Subject, Card


class SubjectCreationForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)


class SubjectDeletionForm(forms.Form):
    to_delete = forms.BooleanField(required=False)


class CardCreationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['front_side_text', 'front_side_img', 'back_side_text', 'back_side_img']

    def is_valid(self):
        valid = super(CardCreationForm, self).is_valid()

        if not valid:
            return False

        if not self.cleaned_data['front_side_text'] and not self.cleaned_data['front_side_img']:
            self.errors['front_side'] = 'Specify text or upload image on front side of card'
            return False

        if not self.cleaned_data['back_side_text'] and not self.cleaned_data['back_side_img']:
            self.errors['back_side'] = 'Specify text or upload image on back side of card'
            return False

        return True


class MarkForm(forms.Form):
    known = forms.BooleanField(required=False)


class CardEditionForm(CardCreationForm):
    to_delete = forms.BooleanField(required=False)

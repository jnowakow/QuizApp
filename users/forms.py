from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Required. Please enter valid email.")
<<<<<<< HEAD
    
    #nested name space for configurations
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
=======
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    # nested name space for configurations
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
>>>>>>> 170e14ae99decbcc65151a59d4c5237512787650

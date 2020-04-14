from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Required. Please enter valid email.")
    
    #nested name space for configurations
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            messages.success(request, f'Account created for {username}!')
            return redirect('Quiz-Home')

    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')
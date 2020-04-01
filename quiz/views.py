from django.shortcuts import render #this will schearch templates directory for html docs


def login(request):
    return render(request, 'quiz/login.html')
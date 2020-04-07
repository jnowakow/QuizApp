from django.shortcuts import render #this will schearch templates directory for html docs


def home(request):
    return render(request, 'quiz/home.html')
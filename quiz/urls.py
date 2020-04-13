from django.urls import path 
from . import views

#the routing of the quiz app

urlpatterns = [
    path('', views.home, name='Quiz-Home'),
    path('details/<int:quizid>/', views.details, name='Quiz-Details'),
    path('question/<int:questionid>/', views.question, name='Quiz-Question'),
    path('add/', views.add, name='Quiz-Add'),
    path('addquestion/<int:quizid>', views.addQuestion, name='Quiz-AddQuestion')
]

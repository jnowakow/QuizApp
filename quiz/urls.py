from django.urls import path 
from . import views

#the routing of the quiz app

urlpatterns = [
    path('', views.start_page, name='Start-Page'),
    path('home/', views.home, name='Quiz-Home'),
    path('details/<int:quizid>/', views.details, name='Quiz-Details'),
    path('question/<int:question_id>/', views.question, name='Quiz-Question'),
    path('add/', views.add, name='Quiz-Add'),
    path('addquestion/<int:quizid>', views.addQuestion, name='Quiz-AddQuestion'),
    path('upload/<int:quizid>', views.upload_quiz, name='Quiz-Upload'),
    path('activatequiz/<int:quizid>', views.activate_quiz, name='Quiz-Activation'),
    path('deactivatequiz/<int:quizid>', views.deactivate_quiz, name='Quiz-Deactivation'),
    path('take/<int:attemptid>', views.take_quiz, name='Take-Quiz'),
    path('attempt/<int:quiz_id>', views.quiz_attempt, name='Quiz-Attempt'),
    path('summary/<int:attemptid>', views.quiz_summary, name='Quiz-Summary'),
    path('stats/<int:quiz_id>', views.statistics, name="Quiz-Stats")
]

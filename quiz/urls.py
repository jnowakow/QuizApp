from django.urls import path 
from . import views

#the routing of the quiz app

urlpatterns = [
    path('', views.login, name='Quiz-Login'),
]

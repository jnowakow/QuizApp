from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Quiz(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    # multipleAnsw = models.BooleanField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

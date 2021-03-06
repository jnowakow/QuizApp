from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Quiz(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()

    # multipleAnsw = models.BooleanField()

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Attempt(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    opponent = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="attempt_opponent")

    def __str__(self):
        return self.id.__str__()


class AttemptQuestion(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author_answered = models.BooleanField(default=False)
    opponent_answered = models.BooleanField(default=True)


# user answer is table connecting Solution with Question and Answer
# each user's answer has a attempt to which it coressponds (Attempt),
# question and answer
class User_Answer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    opponent = models.BooleanField()

    def __str__(self):
        return self.answer.answer

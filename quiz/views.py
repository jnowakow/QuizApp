from django.shortcuts import render, redirect  # this will schearch templates directory for html docs
from .forms import *


def home(request):
    context = {
        'quizes': Quiz.objects.filter()
    }
    return render(request, 'quiz/home.html', context)


def details(request, quizid):
    context = {
        'quiz': Quiz.objects.get(pk=quizid),
        'questions': Quiz.objects.get(pk=quizid).question_set.all()
    }
    return render(request, 'quiz/details.html', context)


def question(request, questionid):
    context = {
        'question': Question.objects.get(pk=questionid)
    }
    return render(request, 'quiz/question.html', context)


def add(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect('Quiz-Home')
    else:
        form = QuizForm()
    return render(request, 'quiz/add.html', {'form': form})


def addQuestion(request, quizid):
    quiz = Quiz.objects.get(pk=quizid)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = quiz.question_set.create(question=form.cleaned_data['question'])
            a1 = q.answer_set.create(answer=form.cleaned_data['answer1'])
            a2 = q.answer_set.create(answer=form.cleaned_data['answer2'])
            q.save()
            a1.save()
            a2.save()
            if form.cleaned_data['answer3']:
                a3 = q.answer_set.create(answer=form.cleaned_data['answer3'])
                a3.save()
            if form.cleaned_data['answer4']:
                a4 = q.answer_set.create(answer=form.cleaned_data['answer4'])
                a4.save()
    else:
        form = QuestionForm()
    context = {
        'form': form,
        'quiz': Quiz.objects.get(pk=quizid),
        'questions': Quiz.objects.get(pk=quizid).question_set.all()
    }
    return render(request, 'quiz/addquestion.html', context)

# this will schearch templates directory for html docs
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *

def start_page(request):
    return render(request, 'quiz/start_page.html')

def home(request):
    context = {
        'quizes': Quiz.objects.filter(),
        'attempts': Attempt.objects.all()
    }
    for attempt in Attempt.objects.all():
        print(attempt)
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

            q = quiz.question_set.create(
                question=form.cleaned_data['question'])
            a1 = q.answer_set.create(
                answer=form.cleaned_data['answer1'], is_correct=form.cleaned_data['is_correct1'])
            a2 = q.answer_set.create(
                answer=form.cleaned_data['answer2'],  is_correct=form.cleaned_data['is_correct2'])
            q.save()
            a1.save()
            a2.save()
            if form.cleaned_data['answer3']:
                a3 = q.answer_set.create(
                    answer=form.cleaned_data['answer3'], is_correct=form.cleaned_data['is_correct3'])
                a3.save()
            if form.cleaned_data['answer4']:
                a4 = q.answer_set.create(
                    answer=form.cleaned_data['answer4'], is_correct=form.cleaned_data['is_correct4'])
                a4.save()
        else:
            error_msg = form._errors.get('no_correct_answer', None)
            if error_msg is not None:
                messages.error(request, error_msg)

    else:
        form = QuestionForm()

    context = {
        'form': form,
        'quiz': Quiz.objects.get(pk=quizid),
        'questions': Quiz.objects.get(pk=quizid).question_set.all()
    }
    return render(request, 'quiz/addquestion.html', context)


def activate_quiz(request, quizid):
    quiz = Quiz.objects.get(pk=quizid)
    quiz.is_active = True
    quiz.save()

    return redirect('Quiz-Home')


def deactivate_quiz(request, quizid):
    quiz = Quiz.objects.get(pk=quizid)
    quiz.is_active = False
    quiz.save()

    return redirect('Quiz-Home')


def answer_question(request, questionid, attemptid):
    question = Question.objects.get(pk=questionid)
    attempt = Attempt.objects.get(pk=attemptid)

    if request.method == 'POST':
        form = UserAnswerForm(request.POST)

        if form.is_valid():
            answers = list(question.answer_set.all())
            answers.sort(key=lambda x: x.pk)

            for answer_num, is_correct in form.cleaned_data.items():
                if is_correct and answer_num == 'is_correct1':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=question, answer=answers[0])

                elif is_correct and answer_num == 'is_correct2':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=question, answer=answers[1])
                    
                elif is_correct and answer_num == 'is_correct3':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=question, answer=answers[2])

                elif is_correct and answer_num == 'is_correct4':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=question, answer=answers[3])

            return redirect('Take-Quiz', attemptid=attemptid)
    else:
        form = UserAnswerForm()
    
    context = {
        'form': form,
        'question': question
    }

    return render(request, 'quiz/answerquestion.html', context=context)


def take_quiz(request, attemptid):
    attempt = Attempt.objects.get(pk=attemptid)
    quiz = attempt.quiz
    context = {
        'quiz': quiz,
        'questions': quiz.question_set.all(),
        'attempt': attempt
    }
    return render(request, 'quiz/take.html', context)


def quiz_attempt(request, quizid):
    quiz = Quiz.objects.get(pk=quizid)

    if request.method == 'POST':
        form = AttemptForm(request.POST)
        
        if form.is_valid() and form.cleaned_data['new_attempt']:
            attempt = quiz.attempt_set.create(author=request.user)
            print("lala")
            return redirect('Quiz-Home')
        
    else:
        form = AttemptForm()

    context = {
        'form': form,
        'quiz':  quiz
    }
    return render(request, 'quiz/attempt.html', context)

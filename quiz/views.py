# this will schearch templates directory for html docs
from django.shortcuts import render, redirect
from django.contrib import messages

from plotly.offline import plot
import plotly.graph_objects as go 

from .forms import *


def start_page(request):
    if request.user.is_authenticated:
        return redirect('Quiz-Home')
    return render(request, 'quiz/start_page.html')


def home(request):
    if not request.user.is_authenticated:
        return redirect('Start-Page')
    
    context = {
        'quizes': Quiz.objects.filter(),
        'attempts': Attempt.objects.all()
    }
    
    return render(request, 'quiz/home.html', context)


def details(request, quizid):
    context = {
        'quiz': Quiz.objects.get(pk=quizid),
        'questions': Quiz.objects.get(pk=quizid).question_set.all()
    }
    return render(request, 'quiz/details.html', context)


def set_initial_edit_form(question, answers):
    initial = {'question': question.question}
    ans = 'answer'
    is_cor = 'is_correct'
    for i in range(len(answers)):
        initial[ans+str(i+1)] = answers[i]
        initial[is_cor+str(i+1)] = answers[i].is_correct

    return initial


def question(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = list(question.answer_set.all())
    answers.sort(key=lambda x: x.pk)
    initial = set_initial_edit_form(question, answers)

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete_question']:
                question.delete()
                return redirect('Quiz-Details', question.quiz.pk)
            else:
                new_question = form.cleaned_data['question']
                if new_question:
                    question.question = new_question
                    question.save()

                if form.cleaned_data['answer1']:
                    answers[0].answer = form.cleaned_data['answer1']
                    answers[0].is_correct = form.cleaned_data['is_correct1']
                    answers[0].save()

                if form.cleaned_data['answer2']:
                    answers[1].answer = form.cleaned_data['answer2']
                    answers[1].is_correct = form.cleaned_data['is_correct2']
                    answers[1].save()

                if form.cleaned_data['answer3']:
                    if len(answers) > 2:
                        answers[2].answer = form.cleaned_data['answer3']
                        answers[2].is_correct = form.cleaned_data['is_correct3']
                        answers[2].save()
                    else:
                        a3 = question.answer_set.create(
                            answer=form.cleaned_data['answer3'], is_correct=form.cleaned_data['is_correct3']
                        )
                        a3.save()
                if form.cleaned_data['answer4']:
                    if len(answers) > 3:
                        answers[3].answer = form.cleaned_data['answer4']
                        answers[3].is_correct = form.cleaned_data['is_correct4']
                        answers[3].save()
                    else:
                        a4 = question.answer_set.create(
                            answer=form.cleaned_data['answer4'], is_correct=form.cleaned_data['is_correct4']
                        )
                        a4.save()
                if form.cleaned_data['delete_answer_1']:
                    answers[0].delete()
                if form.cleaned_data['delete_answer_2']:
                    answers[1].delete()
                if form.cleaned_data['delete_answer_3']:
                    answers[2].delete()
                if form.cleaned_data['delete_answer_4']:
                    answers[3].delete()
        else:
            error_msg = form.errors.get('no_correct_answer', None)
            if error_msg is not None:
                messages.error(request, error_msg)

            error_msg = form.errors.get('question_err', None)
            if error_msg is not None:
                messages.error(request, error_msg)

            error_msg = form.errors.get('answers_num', None)
            if error_msg is not None:
                messages.error(request, error_msg)

            error_msg = form.errors.get('deletion_err', None)
            if error_msg is not None:
                messages.error(request, error_msg)

    else:
        form = EditForm(initial=initial)

    context = {
        'question': question
    }
    if question.quiz.is_editable:
        context['form'] = form
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
                answer=form.cleaned_data['answer2'], is_correct=form.cleaned_data['is_correct2'])
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

            form = QuestionForm()
        else:
            error_msg = form.errors.get('no_correct_answer', None)
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
    quiz.is_editable = False
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
    if User_Answer.objects.filter(attempt_id=attemptid, question_id=questionid).first():
        return redirect('Take-Quiz', attemptid=attemptid)

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
    if attempt.attemptquestion_set.count() == 0:
        return redirect('Quiz-Summary', attemptid)
    aq = attempt.attemptquestion_set.first()
    q = aq.question

    if request.method == 'POST':
        form = UserAnswerForm(request.POST)

        if form.is_valid():
            answers = list(q.answer_set.all())
            answers.sort(key=lambda x: x.pk)

            for answer_num, is_correct in form.cleaned_data.items():
                if is_correct and answer_num == 'is_correct1':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=q, answer=answers[0])

                elif is_correct and answer_num == 'is_correct2':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=q, answer=answers[1])

                elif is_correct and answer_num == 'is_correct3':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=q, answer=answers[2])

                elif is_correct and answer_num == 'is_correct4':
                    user_answer = User_Answer.objects.create(attempt=attempt, question=q, answer=answers[3])
            aq.delete()
            return redirect('Take-Quiz', attemptid=attemptid)
    else:
        form = UserAnswerForm()

    context = {
        'form': form,
        'question': q
    }

    return render(request, 'quiz/answerquestion.html', context=context)


def quiz_attempt(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)

    if request.method == 'POST':
        form = AttemptForm(request.POST)

        if form.is_valid() and form.cleaned_data['new_attempt']:
            attempt = quiz.attempt_set.create(author=request.user)
            questions = quiz.question_set.all()
            for q in questions:
                attempt.attemptquestion_set.create(attempt=attempt, question=q)
            
            return redirect('Take-Quiz', attempt.id)

    else:
        form = AttemptForm()
    context = {
        'form': form,
        'quiz': quiz
    }
    return render(request, 'quiz/attempt.html', context)


class Qna:
    def __init__(self, questionid, attemptid):
        self.q = Question.objects.get(pk=questionid)
        self.a = User_Answer.objects.filter(attempt_id=attemptid, question_id=questionid)
        self.ca = Answer.objects.filter(question=questionid, is_correct=True)

    def get_question(self):
        return self.q

    def get_answer(self):
        return self.a

    def answers_correct(self):
        if self.a.count() != self.ca.count():
            return False
        for ans in self.a:
            if not self.ca.filter(pk=ans.answer.pk).exists():
                return False
        return True


def count_attempt_results(attempt):
    count = 0
    questions = attempt.quiz.question_set.all()
    
    question_stats = {"Question "+str(i+1): 0 for i in range(questions.count())}

    qnas = []
    for question in questions:
        qnas.append(Qna(question.pk, attempt.pk))
    
    for i, qna in enumerate(qnas):
        if qna.answers_correct():
            count += 1 
            key = "Question "+str(i+1)
            question_stats[key] = question_stats[key] + 1

    return qnas, count, question_stats


def quiz_summary(request, attemptid):
  
    attempt = Attempt.objects.get(pk=attemptid)
    qnas, result, questions_stats = count_attempt_results(attempt)

    question_numbers = list(questions_stats.keys())
    right_answers = list(questions_stats.values())
    questions_bar = plot({"data": [go.Bar(x=question_numbers,  y=right_answers, name="Points per question", showlegend=True)],
                          "layout": go.Layout(font=dict(size=16))},
                         output_type='div')

    context = {
        'qnas': qnas,
        'questions_bar': questions_bar,
        'result': result,
        'max': len(qnas)
    }
    return render(request, 'quiz/summary.html', context)


def update_dict(dict1, dict2):
    for key, value in dict2.items():
        dict1[key] = dict1.get(key, 0) + value


def statistics(request, quiz_id):
    attempts = Quiz.objects.get(pk=quiz_id).attempt_set.all()

    stats = dict()
    question_stats = dict()

    for attempt in attempts:
        _, count, q_stats = count_attempt_results(attempt)
        update_dict(question_stats, q_stats)
        stats[count] = stats.get(count, 0) + 1

    results = list(stats.keys())
    users_number = list(stats.values())

    summary_pie = go.Pie(values=users_number,  labels=results, name="Number of users", showlegend=True)

    plot_div = plot({"data": [summary_pie],
                     'layout': go.Layout(legend=dict(title=dict(text='Total result', font=dict(size=20)),
                                                     font=dict(size=20)))}, output_type='div')

    question_numbers = list(question_stats.keys())
    right_answers = list(question_stats.values())
    total_answers = len(attempts)
    wrong_answers = list(map(lambda x: total_answers - x, right_answers))

    correct_answers_bar = go.Bar(x=question_numbers,  y=right_answers, name="Number of correct answers", showlegend=True)
    wrong_answers_bar = go.Bar(x=question_numbers, y=wrong_answers, name='Number of wrong answers', showlegend=True)
    questions_bar = plot({"data": [correct_answers_bar, wrong_answers_bar],
                          "layout": go.Layout(barmode='stack',
                                              xaxis=dict(title='Questions summary', titlefont_size=20),
                                              font=dict(size=16))
                          }, output_type='div')

    context = {
            'plot_div': plot_div,
            'questions_bar': questions_bar,
            'attempts': attempts
            }
    return render(request, "quiz/stats.html", context)



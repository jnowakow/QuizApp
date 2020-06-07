# this will schearch templates directory for html docs
from django.shortcuts import render, redirect, get_object_or_404
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
        initial[ans + str(i + 1)] = answers[i]
        initial[is_cor + str(i + 1)] = answers[i].is_correct

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


def take_quiz(request, attemptid):
    attempt = Attempt.objects.get(pk=attemptid)
    user = request.user
    if attempt.opponent != user and attempt.author != user:
        return redirect('Quiz-Home')
    if attempt.author == user and attempt.attemptquestion_set.filter(
            author_answered=True).count() == attempt.attemptquestion_set.count():
        return redirect('Quiz-Summary', attemptid)
    if attempt.opponent == user and attempt.attemptquestion_set.filter(
            opponent_answered=True).count() == attempt.attemptquestion_set.count():
        return redirect('Quiz-Summary', attemptid)

    if attempt.author == user:
        aq = attempt.attemptquestion_set.filter(author_answered=False).first()
    else:
        aq = attempt.attemptquestion_set.filter(opponent_answered=False).first()
    q = aq.question
    print(q.question)
    form = QuizAnswerForm(request.POST or None, question=q)

    if form.is_valid():
        answers = list(q.answer_set.all())
        answers.sort(key=lambda x: x.pk)

        print(form.cleaned_data['answers'], "abcdf")

        for j in [int(i) for i in form.cleaned_data['answers']]:
            if attempt.author == user:
                User_Answer.objects.create(attempt=attempt, question=q, answer=answers[j], opponent=False)
            else:
                User_Answer.objects.create(attempt=attempt, question=q, answer=answers[j], opponent=True)
        if attempt.author == user:
            aq.author_answered = True
        else:
            aq.opponent_answered = True
        aq.save()
        return redirect('Take-Quiz', attemptid=attemptid)

    context = {
        'form': form,
        'question': q
    }

    return render(request, 'quiz/answerquestion.html', context=context)


def quiz_attempt(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)

    if request.method == 'POST':
        form = AttemptForm(request.POST)

        if form.is_valid():
            attempt = quiz.attempt_set.create(author=request.user)
            questions = quiz.question_set.all()
            if form.cleaned_data["opponent"]:
                attempt.opponent = User.objects.get(username=form.cleaned_data["opponent"])
                attempt.save()
            for q in questions:
                if form.cleaned_data["opponent"]:
                    attempt.attemptquestion_set.create(attempt=attempt, question=q, opponent_answered=False)
                else:
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
        self.a = User_Answer.objects.filter(attempt_id=attemptid, question_id=questionid, opponent=False)
        self.ca = Answer.objects.filter(question=questionid, is_correct=True)
        self.opponentAnswer = User_Answer.objects.filter(attempt_id=attemptid, question_id=questionid, opponent=True)

    def get_question(self):
        return self.q

    def get_answer(self):
        return self.a

    def get_opponent_answer(self):
        return self.opponentAnswer

    def is_answered(self):
        author_answered = self.a.count() != 0
        opponent_answered = self.opponentAnswer.count() != 0
        return author_answered, opponent_answered

    def author_answered(self):
        return self.a.count() != 0

    def opponent_answered(self):
        return self.opponentAnswer.count() != 0

    def author_answers_correct(self):
        if self.a.count() != self.ca.count():
            return False
        for ans in self.a:
            if not self.ca.filter(pk=ans.answer.pk).exists():
                return False
        return True

    def opponent_answers_correct(self):
        if self.opponentAnswer.count() != self.ca.count():
            return False
        for ans in self.opponentAnswer:
            if not self.ca.filter(pk=ans.answer.pk).exists():
                return False
        return True


def count_attempt_results(attempt):
    count = 0
    opponent_count = 0
    questions = attempt.quiz.question_set.all()

    question_stats = {"Question " + str(i + 1): 0 for i in range(questions.count())}
    opponent_stats = {"Question " + str(i + 1): 0 for i in range(questions.count())}

    qnas = []
    for question in questions:
        qnas.append(Qna(question.pk, attempt.pk))

    for i, qna in enumerate(qnas):
        if qna.author_answers_correct():
            count += 1
            key = "Question " + str(i + 1)
            question_stats[key] = 1
        if qna.opponent_answers_correct():
            opponent_count += 1
            key = "Question " + str(i + 1)
            opponent_stats[key] = 1

    return qnas, count, opponent_count, question_stats, opponent_stats


def quiz_summary(request, attemptid):
    attempt = Attempt.objects.get(pk=attemptid)
    qnas, result, opponent_result, questions_stats, opponent_stats = count_attempt_results(attempt)
    author_answered = attempt.attemptquestion_set.filter(
            author_answered=True).count() == attempt.attemptquestion_set.count()
    has_opponent = attempt.opponent is not None
    opponent_answered = attempt.attemptquestion_set.filter(
            opponent_answered=True).count() == attempt.attemptquestion_set.count() and has_opponent
    user = request.user

    if (author_answered and opponent_answered) or not has_opponent:
        for attempt_question in attempt.attemptquestion_set.all():
            attempt_question.delete()

    question_numbers = list(questions_stats.keys())
    right_answers = list(questions_stats.values())
    opponent_answers = list(opponent_stats.values())
    questions_bar = plot({"data": [go.Bar(x=question_numbers, y=right_answers, name="Points", showlegend=True)],
                          "layout": {"title": {"text": attempt.author.username}}},
                         output_type='div')
    if (attempt.opponent is not None):
        questions_bar_o = plot(
            {"data": [go.Bar(x=question_numbers, y=opponent_answers, name="Points", showlegend=True)],
             "layout": {"title": {"text": attempt.opponent.username}}},
            output_type='div')
    else:
        questions_bar_o = None

    if has_opponent:
        opponent = attempt.opponent.username
    else:
        opponent = None
    context = {
        'opponent_answered': opponent_answered,
        'author_answered': author_answered,
        'has_opponent': has_opponent,
        'qnas': qnas,
        'questions_bar': questions_bar,
        'questions_bar_o': questions_bar_o,
        'result': result,
        'opponent_result': opponent_result,
        'max': len(qnas),
        'author': attempt.author.username,
        'opponent': opponent
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
        _, count, opponent_count, q_stats, opponent_stats = count_attempt_results(attempt)
        update_dict(question_stats, q_stats)
        update_dict(question_stats, opponent_stats)
        stats[count] = stats.get(count, 0) + 1
        if attempt.opponent is not None:
            stats[opponent_count] = stats.get(opponent_count, 0) + 1

    results = list(stats.keys())
    users_number = list(stats.values())
    total_users_number = sum(users_number)

    total_correct_diff = list(map(lambda x: total_users_number - x, users_number))
    print(total_correct_diff)

    summary_bar = go.Bar(x=results, y=users_number, name="Number of users", showlegend=True)
    sup_bar = go.Bar(x=results, y=total_correct_diff, name='Supplement to total number', showlegend=True)

    plot_div = plot({"data": [summary_bar, sup_bar],
                     "layout": go.Layout(barmode="stack", xaxis=dict(title='Total points', titlefont_size=16))
                     }, output_type='div')

    question_numbers = list(question_stats.keys())
    right_answers = list(question_stats.values())
    total_answers = 0
    for a in attempts:
        if a.opponent is None:
            total_answers += 1
        else:
            total_answers += 2
    wrong_answers = list(map(lambda x: total_answers - x, right_answers))

    correct_answers_bar = go.Bar(x=question_numbers, y=right_answers, name="Number of correct answers", showlegend=True)
    wrong_answers_bar = go.Bar(x=question_numbers, y=wrong_answers, name='Number of wrong answers', showlegend=True)
    questions_bar = plot({"data": [correct_answers_bar, wrong_answers_bar],
                          "layout": go.Layout(barmode='stack', xaxis=dict(title='Questions summary', titlefont_size=16))
                          }, output_type='div')

    context = {
        'plot_div': plot_div,
        'questions_bar': questions_bar,
        'attempts': attempts
    }
    return render(request, "quiz/stats.html", context)

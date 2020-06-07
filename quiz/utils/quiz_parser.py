from ..models import Quiz

def parse(quiz_file, quiz_id):
    '''
    :param quiz_file: uploaded file with questions to be added
    :param quiz_id: id of quiz to which add questions
    '''

    counter = 0
    quiz = Quiz.objects.get(pk=quiz_id)

    line = quiz_file.readline().strip().decode('utf-8')
    while line:
        if line[0] == 'Q' or line[0] == 'q':
            counter += 1
            question = line
            answer_count = 0
            answers = dict()
            valid_question = False

            line = quiz_file.readline().strip().decode('utf-8')
            while line and (line[0] == 'A' or line[0] == 'a'):
                line = line
                answer_count += 1
                if line[-1] == 'T':
                    valid_question = True
                    answers[answer_count] = (line[:-1], True)
                else:
                    answers[answer_count] = (line, False)

                line = quiz_file.readline().strip().decode('utf-8')

            if 2 <= answer_count <= 4 and valid_question:
                question_obj = quiz.question_set.create(question=question)

                for answer, is_correct in answers.values():
                    question_obj.answer_set.create(answer=answer, is_correct=is_correct)


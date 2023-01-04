from rest_framework.authentication import TokenAuthentication

from ..models import Lesson, Question, QuestionType, Answer, StudentStatics, StudentQuestionStatics
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import CreateQuestionSerializer, GetQuizzSerializer, AnswerQuizzSerializer


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = CreateQuestionSerializer

    @action(detail=True, methods=['get'])
    def list(self, request):
        return Response({"msg": "Get List of Questions"}, status=200)

    @action(detail=True, methods=['POST'])
    def create(self, request):
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            question_type = QuestionType.objects.get(id=request.data['question_type'])
            lesson = Lesson.objects.get(id=request.data['lesson'])
            if question_type.multiple_status is False and len(request.data['answers']) > 1\
                    or question_type.multiple_status is True and len(request.data['answers']) <= 1:
                return Response({"msg": "Data Not Valid"}, status=400)

            question = Question.objects.create(
                content=request.data['content'],
                total_points=request.data['total_points'],
                lesson=lesson,
                question_type=question_type
            )

            for answer in request.data['answers']:
                Answer.objects.create(
                    content=answer['data'],
                    correct=answer['status'],
                    points=0 if answer['status'] is False else answer['points'],
                    question_content=Question.objects.get(id=question.id)
                )
        else:
            return Response({"msg": "Data Not Valid"}, status=400)
        return Response({"msg": "Question added"}, status=201)

    @action(detail=True, methods=['get'])
    def take_quiz(self, request, lesson_id):
        question_array = []
        create_new_status = False
        if not StudentStatics.objects.filter(user=request.user.id, status=True).exists():
            create_new_status = True
            student_statics = StudentStatics.objects.create(
                user=request.user,
                lesson=Lesson.objects.get(id=lesson_id),
                average_score=0,
                progress=0,
                status=True
            )
        questions = Question.objects.filter(lesson=lesson_id)

        for question in questions:
            serializer = GetQuizzSerializer(question)
            question_array.append(serializer.data)

            if create_new_status is True:
                StudentQuestionStatics.objects.create(
                    statics=student_statics,
                    question=question,
                    answer_status=False
                )

        return Response({"data": question_array}, status=200)

    @action(detail=True, methods=['post'])
    def answer_quiz(self, request, lesson_id):
        user = request.user.id
        statics = StudentStatics.objects.get(user=user, status=True)
        quizzs = request.data
        total_score = 0
        answer_array = []
        for answer in quizzs['data']:
            serializer = AnswerQuizzSerializer(data=answer)
            if serializer.is_valid():
                question_id = answer['question_id']
                real_answers = Answer.objects.filter(question_content=question_id, correct=True)\
                    .values_list('id', flat=True)
                real_answers_list = list(real_answers)

                for i in answer['answers']:
                    if i in real_answers_list:
                        real_answers_list.remove(i)
                        answer_array.append({"given_answer": i, "correct": True})
                        answer = Answer.objects.get(id=i, question_content=question_id)
                        answer_point = answer.points
                        total_score = total_score + answer_point
                    else:
                        answer_array.append({"given_answer": i, "correct": False})

                StudentQuestionStatics.objects.filter(statics=statics.id, question=Question.objects.get(id=question_id),)\
                    .update(answer_status=True)
        StudentStatics.objects.filter(user=request.user, status=True).update(
            lesson=Lesson.objects.get(id=lesson_id),
            average_score=total_score / Question.objects.filter(lesson=lesson_id).count(),
            progress=(StudentQuestionStatics.objects
                      .filter(statics=statics.id, answer_status=True).count() /
                      StudentQuestionStatics.objects.filter(statics=statics.id).count()) * 100
        )

        return Response({"total_score": total_score}, status=200)

    @action(detail=True, methods=['post'])
    def reset_quiz(self, request, lesson_id):
        StudentStatics.objects.filter(user=request.user.id, lesson=lesson_id).update(status=False)
        return Response({"msg": "Lesson Progress Reset"}, status=200)
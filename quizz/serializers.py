from rest_framework import serializers
from .models import QuestionType, Question, Answer


class CreateQuestionTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    status = serializers.BooleanField()

    class Meta:
        model = QuestionType
        fields = ['name', 'status']


class CreateLessonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = QuestionType
        fields = ['name']


class CreateQuestionSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=150)
    total_points = serializers.IntegerField()
    lesson = serializers.IntegerField()
    question_type = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ['content', 'total_points', 'lesson', 'question_type']


class GetQuizzSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    total_points = serializers.IntegerField()
    lesson = serializers.CharField(source='lesson.name', read_only=True)
    quesetion_type = serializers.CharField(source='question_type.name', read_only=True)
    choices = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'content', 'total_points', 'lesson', 'quesetion_type', 'choices']

    def get_choices(self, data):
        choice_array = []
        choices = Answer.objects.filter(question_content=data.id).values_list('id', 'content')
        for ch in choices:
            choice_array.append({'id': ch[0], 'content': ch[1]})
        return choice_array


class AnswerQuizzSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    answers = serializers.ListField()

    class Meta:
        model = Question
        fields = ['question_id', 'answers']
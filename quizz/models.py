from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Lesson(models.Model):
    name = models.CharField(max_length=100)


class QuestionType(models.Model):
    name = models.CharField(max_length=100)
    multiple_status = models.BooleanField()


class Question(models.Model):
    content = models.CharField(max_length=150)
    total_points = models.IntegerField()
    lesson = models.ForeignKey("Lesson", default=1, on_delete=models.CASCADE)
    question_type = models.ForeignKey("QuestionType", default=1, on_delete=models.CASCADE)


class Answer(models.Model):
    content = models.CharField(max_length=150)
    correct = models.BooleanField()
    points = models.IntegerField()
    question_content = models.ForeignKey("Question", default=1, on_delete=models.CASCADE)


class StudentStatics(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", default=1, on_delete=models.CASCADE)
    average_score = models.IntegerField()
    progress = models.IntegerField()
    status = models.BooleanField()


class StudentQuestionStatics(models.Model):
    statics = models.ForeignKey("StudentStatics", default=1, on_delete=models.CASCADE)
    question = models.ForeignKey("Question", default=1, on_delete=models.CASCADE)
    answer_status = models.BooleanField()
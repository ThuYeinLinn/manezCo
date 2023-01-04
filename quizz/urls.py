from django.urls import path

from .views import lesson, question_type, question

urlpatterns = [
    path('lesson', lesson.LessonViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='lesson'),
    path('question_type', question_type.QuestionTypeViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='question_type'),
    path('question', question.QuestionViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='question'),
    path('take_quiz/<int:lesson_id>', question.QuestionViewSet.as_view({'get': 'take_quiz'}), name='take_quiz'),
    path('answer_quiz/<int:lesson_id>', question.QuestionViewSet.as_view({'post': 'answer_quiz'}), name='answer_quiz'),
    path('reset_quiz/<int:lesson_id>', question.QuestionViewSet.as_view({'post': 'reset_quiz'}), name='reset_quiz')
]
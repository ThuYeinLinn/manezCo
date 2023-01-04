from rest_framework.authentication import TokenAuthentication

from ..models import Lesson
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import CreateLessonSerializer


class LessonViewSet(viewsets.ModelViewSet):

    queryset = Lesson.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = CreateLessonSerializer

    @action(detail=True, methods=['get'])
    def list(self, request):
        return Response({"msg": "Get Question Type"})

    @action(detail=True, methods=['POST'])
    def create(self, request):
        serializer = CreateLessonSerializer(data=request.data)
        if serializer.is_valid():
            Lesson.objects.create(
                name=request.data['name']
            )
        else:
            return Response({"msg": "Data Not Valid"})
        return Response({"msg": "Lesson added"})
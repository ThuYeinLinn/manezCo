from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from ..models import QuestionType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import CreateQuestionTypeSerializer


class QuestionTypeViewSet(viewsets.ModelViewSet):

    queryset = QuestionType.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = CreateQuestionTypeSerializer

    @action(detail=True, methods=['get'])
    def list(self, request):
        return Response({"msg" : "Get Question Type"})

    @action(detail=True, methods=['POST'])
    def create(self, request):

        user = request.user
        serializer = CreateQuestionTypeSerializer(data=request.data)
        if serializer.is_valid():
            QuestionType.objects.create(
                name=request.data['name'],
                multiple_status=request.data['status']
            )
        else:
            return Response({"msg": "Data Not Valid"})
        return Response({"msg": "QuestionType added"})
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework import viewsets


class AuthenticationViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
            )
            user.set_password(request.data['password'])
            user.save()

            token = Token.objects.create(user=user)
        return JsonResponse({"token": token.key})

    @action(detail=True, methods=['post'])
    def login(self, request):
        username = request.data['username']
        password = request.data['password']
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return HttpResponse(status=400)

        user = authenticate(username=username, password=password)
        if not user:
            return HttpResponse(status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": token.key})

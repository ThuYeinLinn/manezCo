from django.urls import path

from . import views

urlpatterns = [
    path('register', views.AuthenticationViewSet.as_view({'post': 'register'}), name='register_user'),
    path('login', views.AuthenticationViewSet.as_view({'post': 'login'}), name='login_user'),
]
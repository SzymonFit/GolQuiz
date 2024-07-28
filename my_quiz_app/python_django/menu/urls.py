# my_quiz_app/python_django/menu/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('challenge/<int:user_id>/', views.challenge_user, name='challenge_user'),
]
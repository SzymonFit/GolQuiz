# games/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('challenge/<int:user_id>/', views.challenge_user, name='challenge_user'),
    path('menu/', views.menu, name='menu'),
]
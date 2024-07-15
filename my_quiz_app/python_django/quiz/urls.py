
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_user, name='search_user'),
    path('challenge/<int:user_id>/', views.challenge_user, name='challenge_user'),
]
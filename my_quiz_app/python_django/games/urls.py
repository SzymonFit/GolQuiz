# my_quiz_app/python_django/games/urls.py
from django.urls import path
from . import views as games_views

urlpatterns = [
    path('solo/<int:mode>/', games_views.game_solo, name='game_solo'),
    path('random/<int:mode>/', games_views.game_random, name='game_random'),
    path('search/<int:mode>/', games_views.game_search, name='game_search'),
]

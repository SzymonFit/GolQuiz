from django.urls import path
from . import views

urlpatterns = [
    path('solo/create/', views.create_game_solo, name='create_game_solo'),
    path('solo/detail/<int:game_id>/', views.game_solo_detail, name='game_solo_detail'),
    path('random/create/', views.create_game_random, name='create_game_random'),
    path('random/detail/<int:game_id>/', views.game_random_detail, name='game_random_detail'),
    path('search/create/', views.create_game_search, name='create_game_search'),
    path('search/detail/<int:game_id>/', views.game_search_detail, name='game_search_detail'),
]

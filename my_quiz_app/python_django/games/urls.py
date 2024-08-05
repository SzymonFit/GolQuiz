from django.urls import path
from . import views

urlpatterns = [
    path('solo/create/<str:game_mode>/', views.create_game_solo, name='create_game_solo'),
    path('solo/detail/<int:game_id>/', views.game_solo_detail, name='game_solo_detail'),
    path('solo/summary/<int:game_id>/', views.game_solo_summary, name='game_solo_summary'),
    path('random/create/<str:game_mode>/', views.create_game_random, name='create_game_random'),
    path('random/detail/<int:game_id>/', views.game_random_detail, name='game_random_detail'),
    path('random/cancel/<int:game_id>/', views.cancel_game_random, name='cancel_game_random'),
    path('random/join/<str:game_mode>/', views.join_game_random, name='join_game_random'),
    path('random/summary/<int:game_id>/', views.game_random_summary, name='game_random_summary'),
]

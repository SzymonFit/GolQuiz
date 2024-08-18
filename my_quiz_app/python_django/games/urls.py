from django.urls import path, include
from . import views

from .api_views import GameSoloViewSet, GameRandomViewSet, GameSummaryViewSet

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

api_urlpatterns = [
    path('games/solo/', GameSoloViewSet.as_view({
        'post': 'create'
    })),
    path('games/solo/<int:pk>/', GameSoloViewSet.as_view({
        'get': 'retrieve',
        'put': 'update'
    })),
    path('games/random/', GameRandomViewSet.as_view({
        'post': 'create'
    })),
    path('games/random/<int:pk>/', GameRandomViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('games/random/join/<str:game_mode>/', GameRandomViewSet.as_view({
        'get': 'create'
    })),
    path('games/random/cancel/<int:pk>/', GameRandomViewSet.as_view({
        'delete': 'destroy'
    })),
    path('games/summary/<str:game_type>/<int:pk>/', GameSummaryViewSet.as_view({
        'get': 'retrieve'
    })),
]

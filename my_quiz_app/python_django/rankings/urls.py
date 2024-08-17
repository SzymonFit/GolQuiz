from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import RankingView

router = DefaultRouter()

router.register(r'ranking', RankingView, basename='ranking')


urlpatterns = [
    path('<str:game_mode>/', views.ranking_view, name='ranking_view'),
]

api_urlpatterns = [
    path('ranking/<str:game_mode>/', RankingView.as_view(), name='ranking_api_view'),    
]
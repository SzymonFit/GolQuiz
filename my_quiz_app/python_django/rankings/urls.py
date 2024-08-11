from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import RankingViewSet

router = DefaultRouter()

router.register(r'ranking', RankingViewSet, basename='ranking')


urlpatterns = [
    path('<str:game_mode>/', views.ranking_view, name='ranking_view'),
    path('api/', include(router.urls)),
]

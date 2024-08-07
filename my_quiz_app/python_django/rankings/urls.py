from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import UserProfileViewSet

router = DefaultRouter()
router.register(r'user_profiles', UserProfileViewSet, basename='user_profiles')

urlpatterns = [
    path('<str:game_mode>/', views.ranking_view, name='ranking_view'),
    path('', include(router.urls)),
]

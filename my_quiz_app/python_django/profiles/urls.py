# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UserProfileViewSet
from . import views

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('', include(router.urls)),
]

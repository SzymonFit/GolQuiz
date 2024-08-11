# urls.py
from django.urls import path, include
from . import views
from .api_views import ProfileView


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('api/profile/', ProfileView.as_view(), name='api_profile'),
]

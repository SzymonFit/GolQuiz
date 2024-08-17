# urls.py w katalogu profiles
from django.urls import path
from . import views
from .api_views import ProfileView

urlpatterns = [
    path('', views.profile, name='profile'),  # To jest widok HTML
]

api_urlpatterns = [
    path('menu/profile', ProfileView.as_view(), name='api_profile'),  # To jest widok API
]

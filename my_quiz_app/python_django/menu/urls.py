# urls.py
from django.urls import path, include
from . import views
from .api_views import MenuView

urlpatterns = [
    path('', views.menu, name='menu'),
    path('api/menu/', MenuView.as_view(), name='api_menu'),    
]

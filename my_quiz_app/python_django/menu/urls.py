# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UserViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', views.menu, name='menu'),
    path('api/', include(router.urls)),
]

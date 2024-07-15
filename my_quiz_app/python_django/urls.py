"""
URL configuration for my_quiz_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from my_quiz_app.python_django.quiz import views  # Poprawny import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_user, name='search_user'),
    path('challenge/<int:user_id>/', views.challenge_user, name='challenge_user'),
    path('', views.home, name='home'),  # Dodanie ścieżki głównej
    path('logout/', views.logout_view, name='logout'),
]
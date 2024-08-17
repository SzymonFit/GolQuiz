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

# my_quiz_app/urls.py
from django.contrib import admin
from django.urls import path, include
from my_quiz_app.python_django.home import views as home_views
from my_quiz_app.python_django.rankings.views import ranking_view
from my_quiz_app.python_django.users import views as users_views
from my_quiz_app.python_django.profiles import views as profiles_views
from my_quiz_app.python_django.games import views as games_views
from my_quiz_app.python_django.menu import views as menu_views
from my_quiz_app.python_django.rankings import views as rankings_views
from my_quiz_app.python_django.users.urls import api_urlpatterns as users_api_urls
from my_quiz_app.python_django.profiles.urls import api_urlpatterns as profiles_api_urls
from my_quiz_app.python_django.rankings.urls import api_urlpatterns as rankings_api_urls




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('my_quiz_app.python_django.users.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home_views.home, name='home'),
    path('logout/', users_views.logout_view, name='logout'),
    path('profile/', profiles_views.profile, name='profile'),
    path('menu/', menu_views.menu, name='menu'),
    path('menu/', include('my_quiz_app.python_django.menu.urls')), 
    path('games/', include('my_quiz_app.python_django.games.urls')),
    path('ranking/', include('my_quiz_app.python_django.rankings.urls')),
    path('api/', include('my_quiz_app.python_django.home.urls')),
    path('api/', include(users_api_urls)),  # Ścieżki API dla użytkowników
    path('api/', include(profiles_api_urls)),  # Ścieżki API dla profilu,
    path('api/', include(rankings_api_urls)),  # Ścieżka API dla rankingu
]


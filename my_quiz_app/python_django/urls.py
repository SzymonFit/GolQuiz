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
from my_quiz_app.python_django.users import views as users_views
from my_quiz_app.python_django.profiles import views as profiles_views
from my_quiz_app.python_django.games import views as games_views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home_views.home, name='home'),
    path('logout/', users_views.logout_view, name='logout'),
    path('profile/', profiles_views.profile, name='profile'),
    path('search/', profiles_views.search_user, name='search_user'),
    path('challenge/<int:user_id>/', games_views.challenge_user, name='challenge_user'),
    path('menu/', games_views.menu, name='menu'),\
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

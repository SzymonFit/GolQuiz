from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='account_login'),
    path('signup/', views.signup, name='account_signup'),
    path('logout/', views.logout_view, name='account_logout'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]
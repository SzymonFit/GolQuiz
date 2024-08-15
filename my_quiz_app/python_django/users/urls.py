# my_quiz_app/python_django/users/urls.py
from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import UserSignupView, UserLoginView, UserLogoutView, UserViewSet
from .views import set_csrf_token
from .api_views import SetCsrfTokenView
from .api_views import PasswordResetView
from .api_views import PasswordResetConfirmView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# Ścieżki frontendowe
urlpatterns = [
    path('login/', views.login_view, name='account_login'),
    path('signup/', views.signup, name='account_signup'),
    path('logout/', views.logout_view, name='account_logout'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('set-csrf/', set_csrf_token, name='set_csrf'),
]

# Ścieżki API
api_urlpatterns = [
    path('accounts/signup/', UserSignupView.as_view(), name='api_signup'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='api_password_reset'),
    path('accounts/password/reset/done/', views.password_reset_done, name='api_password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='api_password_reset_confirm'),
    path('accounts/password/reset/done/', views.password_reset_complete, name='api_password_reset_complete'),
    path('accounts/set-csrf/', SetCsrfTokenView.as_view(), name='api_set_csrf'),
    path('accounts/', include(router.urls)),
]

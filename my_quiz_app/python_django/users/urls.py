from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import UserSignupView, UserLoginView, UserLogoutView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('login/', views.login_view, name='account_login'),
    path('signup/', views.signup, name='account_signup'),
    path('logout/', views.logout_view, name='account_logout'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('api/signup/', UserSignupView.as_view(), name='api_signup'),
    path('api/login/', UserLoginView.as_view(), name='api_login'),
    path('api/logout/', UserLogoutView.as_view(), name='api_logout'),
    path('api/', include(router.urls)),
]

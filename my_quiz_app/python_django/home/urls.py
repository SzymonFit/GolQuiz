from django.urls import path
from .views import home
from .api_views import LoginAPIView

urlpatterns = [
    path('', home, name='home'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
]

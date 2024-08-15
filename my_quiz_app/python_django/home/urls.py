from django.urls import path
from .views import home
from .api_views import HomeView

urlpatterns = [
    path('', home, name='home'),
    path('home/', HomeView.as_view(), name='api_home'),
]

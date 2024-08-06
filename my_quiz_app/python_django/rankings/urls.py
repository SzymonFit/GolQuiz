from django.urls import path
from . import views

urlpatterns = [
    path('<str:game_mode>/', views.ranking_view, name='ranking_view'),
]

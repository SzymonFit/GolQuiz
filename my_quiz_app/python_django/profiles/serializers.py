from rest_framework import serializers

from my_quiz_app.python_django.menu.serializers import UserSerializer
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Dodajemy UserSerializer jako nested serializer
    total_games = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user',  # Zawiera id, username, email użytkownika
            'total_games',
            'pvp_wins_mode1',
            'pvp_wins_mode2',
            'pvp_wins_mode3',
            'pvp_losses_mode1',
            'pvp_losses_mode2',
            'pvp_losses_mode3',
            'pvp_draws_mode1',
            'pvp_draws_mode2',
            'pvp_draws_mode3',
            'solo_games_played',
            'solo_points_mode1',
            'solo_points_mode2',
            'solo_points_mode3',
            'pvp_points_mode1',
            'pvp_points_mode2',
            'pvp_points_mode3'
        ]

    def get_total_games(self, obj):
        return (
            obj.pvp_wins_mode1 + obj.pvp_losses_mode1 + obj.pvp_draws_mode1 +
            obj.pvp_wins_mode2 + obj.pvp_losses_mode2 + obj.pvp_draws_mode2 +
            obj.pvp_wins_mode3 + obj.pvp_losses_mode3 + obj.pvp_draws_mode3 +
            obj.solo_games_played
        )


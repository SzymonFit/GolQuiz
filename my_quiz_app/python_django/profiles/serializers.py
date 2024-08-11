from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user', 'pvp_wins_mode1', 'pvp_losses_mode1', 'pvp_draws_mode1',
            'pvp_wins_mode2', 'pvp_losses_mode2', 'pvp_draws_mode2',
            'pvp_wins_mode3', 'pvp_losses_mode3', 'pvp_draws_mode3',
            'solo_games_played'
        ]
        depth = 1  # To serialize the related user model

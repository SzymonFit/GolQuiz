# serializers.py
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'pvp_wins_mode1', 'pvp_wins_mode2', 'pvp_wins_mode3',
                  'pvp_losses_mode1', 'pvp_losses_mode2', 'pvp_losses_mode3',
                  'pvp_draws_mode1', 'pvp_draws_mode2', 'pvp_draws_mode3',
                  'solo_games_played', 'email', 'solo_points_mode1', 'solo_points_mode2',
                  'solo_points_mode3', 'pvp_points_mode1', 'pvp_points_mode2', 'pvp_points_mode3']

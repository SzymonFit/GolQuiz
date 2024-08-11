from rest_framework import serializers
from my_quiz_app.python_django.profiles.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['username', 'pvp_points_mode1', 'pvp_points_mode2', 'pvp_points_mode3', 
                  'pvp_wins_mode1', 'pvp_wins_mode2', 'pvp_wins_mode3', 
                  'pvp_losses_mode1', 'pvp_losses_mode2', 'pvp_losses_mode3', 
                  'pvp_draws_mode1', 'pvp_draws_mode2', 'pvp_draws_mode3']

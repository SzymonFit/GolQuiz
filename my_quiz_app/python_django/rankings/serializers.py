from rest_framework import serializers
from my_quiz_app.python_django.profiles.models import UserProfile

class RankingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    position = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'pvp_points_mode1', 'pvp_points_mode2', 'pvp_points_mode3', 
                  'pvp_wins_mode1', 'pvp_wins_mode2', 'pvp_wins_mode3', 
                  'pvp_losses_mode1', 'pvp_losses_mode2', 'pvp_losses_mode3', 
                  'pvp_draws_mode1', 'pvp_draws_mode2', 'pvp_draws_mode3',
                  'position']

    def get_position(self, obj):
        # To pole możesz wypełnić informacją o miejscu użytkownika w rankingu.
        # Przykładowo, możesz dodać tę informację, jeśli przekazujesz miejsce użytkownika
        # jako część kontekstu do serializera.
        if 'position' in self.context:
            return self.context['position']
        return None

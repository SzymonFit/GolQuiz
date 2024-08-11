from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        total_games = (
            profile.pvp_wins_mode1 + profile.pvp_losses_mode1 + profile.pvp_draws_mode1 +
            profile.pvp_wins_mode2 + profile.pvp_losses_mode2 + profile.pvp_draws_mode2 +
            profile.pvp_wins_mode3 + profile.pvp_losses_mode3 + profile.pvp_draws_mode3 + profile.solo_games_played
        )

        serializer = UserProfileSerializer(profile)
        data = serializer.data
        data['total_games'] = total_games

        return Response(data)

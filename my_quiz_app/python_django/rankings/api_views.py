from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RankingSerializer
from my_quiz_app.python_django.profiles.models import UserProfile


class RankingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, game_mode):
        # Zmapuj wartości game_mode na odpowiednie pola w modelu UserProfile
        mode_to_field_map = {
            "mode1": "pvp_points_mode1",
            "mode2": "pvp_points_mode2",
            "mode3": "pvp_points_mode3"
        }

        # Pobierz odpowiednie pole na podstawie wartości game_mode
        order_field = mode_to_field_map.get(game_mode)

        if not order_field:
            return Response({"error": "Invalid game mode"}, status=400)

        # Użyj order_field do posortowania wyników
        profiles = UserProfile.objects.all().order_by(f'-{order_field}')

        serialized_data = []
        user_position = None
        for index, profile in enumerate(profiles, start=1):
            serializer = RankingSerializer(profile, context={'position': index})
            serialized_data.append(serializer.data)

            # Sprawdź, czy bieżący profil należy do zalogowanego użytkownika
            if profile.user == request.user:
                user_position = index

        # Dodaj user_position do odpowiedzi
        return Response({
            'users': serialized_data,
            'user_position': user_position,
        })

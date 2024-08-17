# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from my_quiz_app.python_django.profiles.models import UserProfile
# from django.db.models import Q
# from .serializers import UserProfileSerializer

# class RankingViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request, game_mode=None):
#         search_query = request.GET.get('q', '')
#         if game_mode not in ['mode1', 'mode2', 'mode3']:
#             return Response({"error": "Nieprawidłowy tryb gry"}, status=400)

#         if game_mode == 'mode1':
#             order_by = '-pvp_points_mode1'
#         elif game_mode == 'mode2':
#             order_by = '-pvp_points_mode2'
#         else:
#             order_by = '-pvp_points_mode3'

#         all_users = UserProfile.objects.order_by(order_by)
#         user_positions = {user.user.username: idx + 1 for idx, user in enumerate(all_users)}

#         if search_query:
#             filtered_users = all_users.filter(Q(user__username__icontains=search_query))
#         else:
#             filtered_users = all_users

#         serializer = UserProfileSerializer(filtered_users, many=True)
#         response_data = serializer.data

#         for user_data in response_data:
#             username = user_data['username']
#             user_data['position'] = user_positions.get(username, None)

#         user_position = user_positions.get(request.user.username, None)

#         return Response({
#             'users': response_data,
#             'user_position': user_position,
#         })
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
        for index, profile in enumerate(profiles, start=1):
            serializer = RankingSerializer(profile, context={'position': index})
            serialized_data.append(serializer.data)

        return Response(serialized_data)

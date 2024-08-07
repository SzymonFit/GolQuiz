from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import Q
from my_quiz_app.python_django.profiles.models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get'])
    def rankings(self, request, game_mode=None):
        search_query = request.GET.get('q', '')
        if game_mode not in ['mode1', 'mode2', 'mode3']:
            return Response({"error": "Invalid game mode"}, status=400)

        if game_mode == 'mode1':
            order_by = '-pvp_points_mode1'
        elif game_mode == 'mode2':
            order_by = '-pvp_points_mode2'
        else:
            order_by = '-pvp_points_mode3'

        users = UserProfile.objects.filter(
            Q(user__username__icontains=search_query)
        ).order_by(order_by)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def position(self, request, pk=None):
        user = self.get_object()
        game_mode = request.GET.get('game_mode', 'mode1')
        if game_mode not in ['mode1', 'mode2', 'mode3']:
            return Response({"error": "Invalid game mode"}, status=400)

        if game_mode == 'mode1':
            order_by = '-pvp_points_mode1'
        elif game_mode == 'mode2':
            order_by = '-pvp_points_mode2'
        else:
            order_by = '-pvp_points_mode3'

        all_users = UserProfile.objects.order_by(order_by)
        user_positions = {user.user.username: idx + 1 for idx, user in enumerate(all_users)}
        position = user_positions.get(user.user.username, None)

        return Response({"position": position})


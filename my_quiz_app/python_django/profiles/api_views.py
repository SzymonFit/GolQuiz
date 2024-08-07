# api_views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def get_profile(self, request):
        profile = self.get_queryset().get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

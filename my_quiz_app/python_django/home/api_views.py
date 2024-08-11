from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import status
from .serializers import AuthLoginSerializer

class HomeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user is not None:
                login(request, user)
                return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"detail": "User is already authenticated"}, status=status.HTTP_200_OK)
        return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

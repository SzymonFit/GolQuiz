from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login as auth_login, logout, authenticate, login
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .serializers import UserSerializer, UserLoginSerializer, UserSignupSerializer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
# Zmienna używana do tokenów sesji resetowania hasła
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


User = get_user_model()



class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class SetCsrfTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        csrf_token = request.META.get('CSRF_COOKIE', None)
        print(csrf_token)
        return Response({'csrfToken': csrf_token}, status=200)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                # Generowanie tokenu do resetu hasła
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Składanie URL do resetu hasła (musisz dostosować to do swojego frontendu)
                reset_url = f"http://localhost:4200/api/accounts/reset/{uid}/{token}/"
                
                # Wysyłanie emaila z linkiem do resetu hasła
                send_mail(
                    subject="Reset your password",
                    message=f"Click the link to reset your password: {reset_url}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                
                logger.info(f"Password reset email sent to {email}.")
                return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"No user found with email: {email}")
                return Response({"detail": "No user found with this email address."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error("Email field is required.")
            return Response({"detail": "Email field is required."}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetDoneView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Password reset process done."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    token_generator = default_token_generator
    success_url = '/api/accounts/password/reset/complete/'  # URL sukcesu

    @method_decorator(csrf_protect)
    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        if not uidb64 or not token:
            return Response({"detail": "Missing UID or token."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Dekodowanie UID i wyszukiwanie użytkownika
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid UID."}, status=status.HTTP_400_BAD_REQUEST)

        # Sprawdzenie poprawności tokena
        if not self.token_generator.check_token(user, token):
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        # Pobranie nowego hasła z żądania
        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"detail": "New password not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Ustawienie nowego hasła i zapisanie użytkownika w bazie danych
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)

class PasswordResetCompleteView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Password reset complete."}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

from rest_framework import serializers
from my_quiz_app.python_django.profiles.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

# serializers.py
from rest_framework import serializers
from .models import GameSolo, GameRandom

class GameSoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSolo
        fields = '__all__'

class GameRandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRandom
        fields = '__all__'

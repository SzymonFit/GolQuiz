from rest_framework import serializers
from .models import GameSolo, GameRandom

class GameSoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSolo
        fields = ['id', 'player1', 'score_player1', 'questions_answered_player1', 'game_mode', 'questions', 'end_time']

class GameRandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRandom
        fields = ['id', 'player1', 'player2', 'score_player1', 'score_player2', 'questions_answered_player1', 'questions_answered_player2', 'game_mode', 'questions', 'end_time', 'points_updated']

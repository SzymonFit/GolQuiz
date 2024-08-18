from django.contrib import admin
from .models import GameSolo, GameRandom

@admin.register(GameSolo)
class GameSoloAdmin(admin.ModelAdmin):
    list_display = ['id', 'player1', 'score_player1', 'game_mode', 'questions_answered_player1', 'start_time', 'end_time', 'is_solo']
    search_fields = ['player1__username', 'game_mode']
    list_filter = ['game_mode', 'end_time']

@admin.register(GameRandom)
class GameRandomAdmin(admin.ModelAdmin):
    list_display = ['id', 'player1', 'player2', 'score_player1', 'score_player2', 'game_mode', 'questions_answered_player1', 'questions_answered_player2','start_time', 'end_time', 'points_updated']
    search_fields = ['player1__username', 'player2__username', 'game_mode']
    list_filter = ['game_mode', 'end_time', 'points_updated']

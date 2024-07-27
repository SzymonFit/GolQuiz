# games/models.py
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    player1 = models.ForeignKey(User, related_name='game_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='game_player2', on_delete=models.CASCADE, null=True, blank=True)
    score_player1 = models.IntegerField(default=0)
    score_player2 = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    mode = models.IntegerField(default=0)

    def __str__(self):
        return f'Game {self.id} - {self.player1} vs {self.player2}'

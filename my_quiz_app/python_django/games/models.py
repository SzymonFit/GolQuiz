from django.db import models
from django.contrib.auth.models import User

class GameBase(models.Model):
    player1 = models.ForeignKey(User, related_name='%(class)s_player1', on_delete=models.CASCADE)
    score_player1 = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    questions_answered_player1 = models.IntegerField(default=0)
    questions_answered_player2 = models.IntegerField(default=0)
    questions = models.JSONField(default=list)
    game_mode = models.CharField(max_length=20)

    class Meta:
        abstract = True

class GameSolo(GameBase):
    is_solo = models.BooleanField(default=True)

    def __str__(self):
        return f'Solo Game {self.id} - {self.player1}'

class GameRandom(GameBase):
    player2 = models.ForeignKey(User, related_name='game_random_player2', on_delete=models.CASCADE, null=True, blank=True)
    score_player2 = models.IntegerField(default=0)
    questions_answered = models.IntegerField(default=0)
    points_updated = models.BooleanField(default=False)
    

    def __str__(self):
        return f'Random Game {self.id} - {self.player1} vs {self.player2}'

# my_quiz_app/python_django/games/models.py
from django.db import models
from django.conf import settings

class Game(models.Model):
    player1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    
    def __str__(self):
        return f"{self.player1} vs {self.player2}"

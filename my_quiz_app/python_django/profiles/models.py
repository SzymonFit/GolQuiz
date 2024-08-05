# profiles/models.py

from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    pvp_wins_mode1 = models.IntegerField(default=0)
    pvp_wins_mode2 = models.IntegerField(default=0)
    pvp_wins_mode3 = models.IntegerField(default=0)
    pvp_losses_mode1 = models.IntegerField(default=0)
    pvp_losses_mode2 = models.IntegerField(default=0)
    pvp_losses_mode3 = models.IntegerField(default=0)
    pvp_draws_mode1 = models.IntegerField(default=0)
    pvp_draws_mode2 = models.IntegerField(default=0)
    pvp_draws_mode3 = models.IntegerField(default=0)

    solo_games_played = models.IntegerField(default=0)
    email = models.EmailField()

    # Punkty zdobyte w trybach solo
    solo_points_mode1 = models.IntegerField(default=0)
    solo_points_mode2 = models.IntegerField(default=0)
    solo_points_mode3 = models.IntegerField(default=0)

    # Punkty zdobyte w trybach PvP
    pvp_points_mode1 = models.IntegerField(default=0)
    pvp_points_mode2 = models.IntegerField(default=0)
    pvp_points_mode3 = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

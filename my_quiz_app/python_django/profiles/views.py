from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile(request):
    profile = request.user.userprofile
    total_games = (
        profile.pvp_wins_mode1 + profile.pvp_losses_mode1 + profile.pvp_draws_mode1 +
        profile.pvp_wins_mode2 + profile.pvp_losses_mode2 + profile.pvp_draws_mode2 +
        profile.pvp_wins_mode3 + profile.pvp_losses_mode3 + profile.pvp_draws_mode3 + profile.solo_games_played
    )  # Obliczenie liczby zagranych gier
    return render(request, 'profiles/profile.html', {'profile': profile, 'total_games': total_games})

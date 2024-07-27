# profiles/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile(request):
    profile = request.user.userprofile
    total_games = profile.wins + profile.losses + profile.draws  # Obliczenie liczby zagranych gier
    return render(request, 'profiles/profile.html', {'profile': profile, 'total_games': total_games})

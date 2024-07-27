# games/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Game

@login_required
def game_solo(request, mode):
    # Implementacja logiki dla gry solo
    return render(request, 'games/game_solo.html', {'mode': mode})

@login_required
def game_random(request, mode):
    # Implementacja logiki dla wyszukiwania losowego przeciwnika
    return render(request, 'games/game_random.html', {'mode': mode})

@login_required
def game_search(request, mode):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            opponent = User.objects.get(username=username)
            # Implementacja logiki dla wyszukiwania przeciwnika po loginie
            return render(request, 'games/game_search.html', {'mode': mode, 'opponent': opponent})
        except User.DoesNotExist:
            return render(request, 'games/game_search.html', {'mode': mode, 'error': 'User not found'})
    return render(request, 'games/game_search.html', {'mode': mode})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.db.models import Q
from my_quiz_app.python_django.quiz.models import Game, UserProfile, User

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'home.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    profile = request.user.userprofile
    return render(request, 'quiz/profile.html', {'profile': profile})

def search_user(request):
    query = request.GET.get('query')
    if query:
        results = UserProfile.objects.filter(Q(user__username__icontains=query) | Q(special_id__icontains=query))
    else:
        results = []
    return render(request, 'quiz/search.html', {'results': results})

@login_required
def challenge_user(request, user_id):
    opponent = get_object_or_404(User, id=user_id)
    Game.objects.create(player1=request.user, player2=opponent)
    return redirect('profile')
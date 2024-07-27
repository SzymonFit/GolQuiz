from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from my_quiz_app.python_django.profiles.models import UserProfile

@login_required
def menu(request):
    user = request.user
    return render(request, 'menu/menu.html', {'user': user})

# @login_required
# def challenge_user(request, user_id):
#     opponent = get_object_or_404(User, id=user_id)
#     Game.objects.create(player1=request.user, player2=opponent)
#     return redirect('profile')

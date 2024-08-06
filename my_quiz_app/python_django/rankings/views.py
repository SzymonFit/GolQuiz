from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from my_quiz_app.python_django.profiles.models import UserProfile

@login_required
def ranking_view(request, game_mode):
    search_query = request.GET.get('q', '')
    if game_mode not in ['mode1', 'mode2', 'mode3']:
        raise ValueError("Nieprawidłowy tryb gry")

    if game_mode == 'mode1':
        order_by = '-pvp_points_mode1'
        points_field = 'pvp_points_mode1'
        wins_field = 'pvp_wins_mode1'
        losses_field = 'pvp_losses_mode1'
        draws_field = 'pvp_draws_mode1'
    elif game_mode == 'mode2':
        order_by = '-pvp_points_mode2'
        points_field = 'pvp_points_mode2'
        wins_field = 'pvp_wins_mode2'
        losses_field = 'pvp_losses_mode2'
        draws_field = 'pvp_draws_mode2'
    else:
        order_by = '-pvp_points_mode3'
        points_field = 'pvp_points_mode3'
        wins_field = 'pvp_wins_mode3'
        losses_field = 'pvp_losses_mode3'
        draws_field = 'pvp_draws_mode3'

    all_users = UserProfile.objects.order_by(order_by)
    user_positions = {user.user.username: idx + 1 for idx, user in enumerate(all_users)}

    if search_query:
        filtered_users = all_users.filter(Q(user__username__icontains=search_query))
    else:
        filtered_users = all_users

    for user in filtered_users:
        user.position = user_positions[user.user.username]

    user_position = user_positions.get(request.user.username, None)

    context = {
        'users': filtered_users,
        'user_position': user_position,
        'points_field': points_field,
        'wins_field': wins_field,
        'losses_field': losses_field,
        'draws_field': draws_field,
        'game_mode': game_mode,
    }
    return render(request, 'rankings/ranking.html', context)

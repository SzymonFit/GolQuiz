import random
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import GameSolo, GameRandom
from .questions import get_random_question, check_answer, load_questions, generate_question
from my_quiz_app.python_django.profiles.models import UserProfile

logger = logging.getLogger(__name__)

@login_required
def create_game_solo(request, game_mode):
    game = GameSolo.objects.create(player1=request.user, game_mode=game_mode)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.solo_games_played += 1
    profile.save()

    if game_mode == 'mode1' or game_mode == 'mode2':
        questions = load_questions(game_mode)
        random_questions = [generate_question(random.choice(questions), random.randint(0, 9), game_mode) for _ in range(10)]
    elif game_mode == 'mode3':
        random_questions = [get_random_question(random.choice(['mode1', 'mode2'])) for _ in range(10)]
    else:
        raise ValueError("Invalid game mode")

    request.session['game_solo_questions'] = random_questions
    logger.debug(f"Generated Questions for Solo Game: {random_questions}")

    return redirect('game_solo_detail', game_id=game.id)

@login_required
def game_solo_detail(request, game_id):
    game = get_object_or_404(GameSolo, id=game_id)
    questions = request.session.get('game_solo_questions', [])
    current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if current_question:
            correct = check_answer(current_question, answer)
            game.questions.append({
                'question': current_question['question'],
                'correct_answer': current_question['correct_answer'],
                'user_answer': answer,
                'is_correct': correct
            })

            if correct:
                game.score_player1 += 1
            
            game.questions_answered_player1 += 1
            game.save()

            if game.questions_answered_player1 < 10:
                return redirect('game_solo_detail', game_id=game.id)
            else:
                game.end_time = timezone.now()
                game.save()
                
                # Update user profile based on game mode
                profile = request.user.userprofile
                if game.game_mode == 'mode1':
                    profile.solo_points_mode1 += game.score_player1
                elif game.game_mode == 'mode2':
                    profile.solo_points_mode2 += game.score_player1
                elif game.game_mode == 'mode3':
                    profile.solo_points_mode3 += game.score_player1
                profile.save()
                
                return redirect('game_solo_summary', game_id=game.id)

    return render(request, 'games/game_solo.html', {'game': game, 'question': current_question})

@login_required
def create_game_random(request, game_mode):
    existing_game = GameRandom.objects.filter(player2__isnull=True, game_mode=game_mode).exclude(player1=request.user).first()

    if existing_game:
        existing_game.player2 = request.user
        existing_game.save()
        # Ustaw pytania, jeśli jeszcze nie są ustawione
        if not existing_game.questions:
            questions = [get_random_question(game_mode) for _ in range(10)]
            existing_game.questions = questions
            existing_game.save()
        # Notify both players to start the game
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'game_{existing_game.id}',
            {
                'type': 'game_message',
                'message': 'opponent_joined'
            }
        )
        return JsonResponse({'redirect_url': f'/games/random/detail/{existing_game.id}/'})
    else:
        game = GameRandom.objects.create(player1=request.user, game_mode=game_mode)
        # Generate questions when creating a new game
        questions = [get_random_question(game_mode) for _ in range(10)]
        game.questions = questions
        game.save()
        return JsonResponse({'message': 'Waiting for an opponent...', 'game_id': game.id})

@login_required
def join_game_random(request, game_mode):
    logger.debug(f"User {request.user.username} is trying to join a random game in mode {game_mode}")

    existing_game = GameRandom.objects.filter(player2__isnull=True, game_mode=game_mode).exclude(player1=request.user).exclude(player2=request.user).first()

    if existing_game:
        existing_game.player2 = request.user
        existing_game.save()
        logger.debug(f"User {request.user.username} joined game ID {existing_game.id} as player2")
        # Notify both players to start the game
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'game_{existing_game.id}',
            {
                'type': 'game_message',
                'message': 'opponent_joined'
            }
        )
        return JsonResponse({'redirect_url': f'/games/random/detail/{existing_game.id}/'})
    else:
        game = GameRandom.objects.create(player1=request.user, game_mode=game_mode)
        questions = [get_random_question(game_mode) for _ in range(10)]
        game.questions = questions
        game.save()
        logger.debug(f"User {request.user.username} created a new game ID {game.id} as player1")
        return JsonResponse({'message': 'Waiting for an opponent...', 'game_id': game.id})

@login_required
def cancel_game_random(request, game_id):
    game = get_object_or_404(GameRandom, id=game_id)
    if game.player1 == request.user and game.player2 is None:
        game.delete()
        logger.debug(f"User {request.user.username} canceled game ID {game_id}")
        return JsonResponse({'message': 'Game canceled'})
    return JsonResponse({'message': 'Cannot cancel the game'})

@login_required
def game_random_detail(request, game_id):
    game = get_object_or_404(GameRandom, id=game_id)

    if request.user not in [game.player1, game.player2]:
        return redirect('menu')

    if game.player2 is None:
        return JsonResponse({'message': 'Waiting for an opponent...'})

    questions = game.questions

    if request.user == game.player1:
        current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None
    else:
        current_question = questions[game.questions_answered_player2] if game.questions_answered_player2 < len(questions) else None

    logger.debug(f"User: {request.user.username}, Current Question: {current_question}, Questions: {questions}")

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if current_question:
            is_correct = check_answer(current_question, answer)
            question_data = {
                'question': current_question['question'],
                'correct_answer': current_question['correct_answer'],
                'user_answer': answer,
                'is_correct': is_correct,
                'player': 'player1' if request.user == game.player1 else 'player2'
            }
            if request.user == game.player1:
                game.questions_answered_player1 += 1
                game.questions.append(question_data)
                if is_correct:
                    game.score_player1 += 1
            else:
                game.questions_answered_player2 += 1
                game.questions.append(question_data)
                if is_correct:
                    game.score_player2 += 1
            
            game.save()

        if game.questions_answered_player1 >= 10 and game.questions_answered_player2 >= 10:
            game.end_time = timezone.now()
            game.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'game_{game.id}',
                {
                    'type': 'game_message',
                    'message': 'game_ended'
                }
            )
            return redirect('game_random_summary', game_id=game.id)

        if (request.user == game.player1 and game.questions_answered_player1 >= 10) or (request.user == game.player2 and game.questions_answered_player2 >= 10):
            waiting_message = 'Proszę czekać na drugiego gracza...'
            return render(request, 'games/game_pvp.html', {'game': game, 'waiting_message': waiting_message, 'question': None})

        return redirect('game_random_detail', game_id=game.id)

    return render(request, 'games/game_pvp.html', {'game': game, 'question': current_question})

@login_required
def game_solo_summary(request, game_id):
    game = get_object_or_404(GameSolo, id=game_id)
    return render(request, 'games/game_solo_summary.html', {'game': game})

@login_required
def game_random_summary(request, game_id):
    game = get_object_or_404(GameRandom, id=game_id)
    result = None
    game_mode = game.game_mode

    profile1 = UserProfile.objects.get(user=game.player1)
    profile2 = UserProfile.objects.get(user=game.player2)

    logger.debug(f"Game {game_id} summary: Player1: {game.player1.username}, Player2: {game.player2.username}")
    logger.debug(f"Scores: Player1: {game.score_player1}, Player2: {game.score_player2}")

    if game.score_player1 > game.score_player2:
        result = f"{game.player1.username} wins!"
        if game_mode == 'mode1':
            profile1.pvp_wins_mode1 += 1
            profile1.pvp_points_mode1 += game.score_player1
            profile2.pvp_losses_mode1 += 1
            profile2.pvp_points_mode1 += game.score_player2
        elif game_mode == 'mode2':
            profile1.pvp_wins_mode2 += 1
            profile1.pvp_points_mode2 += game.score_player1
            profile2.pvp_losses_mode2 += 1
            profile2.pvp_points_mode2 += game.score_player2
        elif game_mode == 'mode3':
            profile1.pvp_wins_mode3 += 1
            profile1.pvp_points_mode3 += game.score_player1
            profile2.pvp_losses_mode3 += 1
            profile2.pvp_points_mode3 += game.score_player2
        logger.debug(f"Winner points added: {game.score_player1}, Loser points added: {game.score_player2}")
    elif game.score_player1 < game.score_player2:
        result = f"{game.player2.username} wins!"
        if game_mode == 'mode1':
            profile2.pvp_wins_mode1 += 1
            profile2.pvp_points_mode1 += game.score_player2
            profile1.pvp_losses_mode1 += 1
            profile1.pvp_points_mode1 += game.score_player1
        elif game_mode == 'mode2':
            profile2.pvp_wins_mode2 += 1
            profile2.pvp_points_mode2 += game.score_player2
            profile1.pvp_losses_mode2 += 1
            profile1.pvp_points_mode2 += game.score_player1
        elif game_mode == 'mode3':
            profile2.pvp_wins_mode3 += 1
            profile2.pvp_points_mode3 += game.score_player2
            profile1.pvp_losses_mode3 += 1
            profile1.pvp_points_mode3 += game.score_player1
        logger.debug(f"Winner points added: {game.score_player2}, Loser points added: {game.score_player1}")
    else:
        result = "It's a tie!"
        if game_mode == 'mode1':
            profile1.pvp_draws_mode1 += 1
            profile1.pvp_points_mode1 += game.score_player1
            profile2.pvp_draws_mode1 += 1
            profile2.pvp_points_mode1 += game.score_player2
        elif game_mode == 'mode2':
            profile1.pvp_draws_mode2 += 1
            profile1.pvp_points_mode2 += game.score_player1
            profile2.pvp_draws_mode2 += 1
            profile2.pvp_points_mode2 += game.score_player2
        elif game_mode == 'mode3':
            profile1.pvp_draws_mode3 += 1
            profile1.pvp_points_mode3 += game.score_player1
            profile2.pvp_draws_mode3 += 1
            profile2.pvp_points_mode3 += game.score_player2
        logger.debug(f"Tie points added: Player1: {game.score_player1}, Player2: {game.score_player2}")

    profile1.save()
    profile2.save()

    player1_questions = [q for q in game.questions if q.get('player') == 'player1']
    player2_questions = [q for q in game.questions if q.get('player') == 'player2']

    return render(request, 'games/game_pvp_summary.html', {
        'game': game,
        'result': result,
        'player1_questions': player1_questions,
        'player2_questions': player2_questions,
    })
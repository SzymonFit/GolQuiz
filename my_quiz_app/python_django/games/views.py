import random
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import GameSolo, GameRandom, GameSearch
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
def create_game_search(request, game_mode):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            opponent = User.objects.get(username=username)
            game = GameSearch.objects.create(player1=request.user, player2=opponent, game_mode=game_mode)
            return redirect('game_search_detail', game_id=game.id)
        except User.DoesNotExist:
            return render(request, 'games/game_search.html', {'error': 'User not found'})
    return render(request, 'games/game_search.html')

@login_required
def game_search_detail(request, game_id):
    game = get_object_or_404(GameSearch, id=game_id)
    if request.user not in [game.player1, game.player2]:
        return redirect('menu')

    question = get_random_question(game.game_mode)

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if check_answer(question, answer):
            if request.user == game.player1:
                game.score_player1 += 1
                game.questions_answered_player1 += 1
            else:
                game.score_player2 += 1
                game.questions_answered_player2 += 1
            game.save()
            if game.questions_answered_player1 >= 10 and game.questions_answered_player2 >= 10:
                game.end_time = timezone.now()
                game.save()
                return redirect('game_search_summary', game_id=game.id)
            return redirect('game_search_detail', game_id=game.id)

    return render(request, 'games/game_pvp.html', {'game': game, 'question': question})

@login_required
def game_solo_summary(request, game_id):
    game = get_object_or_404(GameSolo, id=game_id)
    return render(request, 'games/game_solo_summary.html', {'game': game})

@login_required
def game_random_summary(request, game_id):
    game = get_object_or_404(GameRandom, id=game_id)
    result = None
    if game.score_player1 > game.score_player2:
        result = f"{game.player1.username} wins!"
    elif game.score_player1 < game.score_player2:
        result = f"{game.player2.username} wins!"
    else:
        result = "It's a tie!"

    player1_questions = [q for q in game.questions if q.get('player') == 'player1']
    player2_questions = [q for q in game.questions if q.get('player') == 'player2']

    return render(request, 'games/game_pvp_summary.html', {
        'game': game,
        'result': result,
        'player1_questions': player1_questions,
        'player2_questions': player2_questions,
    })


@login_required
def game_search_summary(request, game_id):
    game = get_object_or_404(GameSearch, id=game_id)
    result = None
    if game.score_player1 > game.score_player2:
        result = f"{game.player1.username} wins!"
    elif game.score_player1 < game.score_player2:
        result = f"{game.player2.username} wins!"
    else:
        result = "It's a tie!"

    return render(request, 'games/game_pvp_summary.html', {'game': game, 'result': result})

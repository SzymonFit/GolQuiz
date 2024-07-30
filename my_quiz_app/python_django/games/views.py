from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import GameSolo, GameRandom, GameSearch
from my_quiz_app.python_django.profiles.models import UserProfile
from .questions import get_random_question, check_answer, load_questions, generate_question
import random

@login_required
def create_game_solo(request, game_mode):
    game = GameSolo.objects.create(player1=request.user, game_mode=game_mode)
    
    # Update user profile statistics
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.solo_games_played += 1
    profile.save()

    # Generate random questions for the game based on the selected game mode 
    if game_mode == 'mode1' or game_mode == 'mode2':
        questions = load_questions(game_mode)
        random_questions = [generate_question(random.choice(questions), random.randint(0, 9), game_mode) for _ in range(10)]
    elif game_mode == 'mode3':
        random_questions = [get_random_question(random.choice(['mode1', 'mode2'])) for _ in range(10)]
    else:
        raise ValueError("Invalid game mode")

    request.session['game_solo_questions'] = random_questions

    return redirect('game_solo_detail', game_id=game.id)

@login_required
def game_solo_detail(request, game_id):
    game = get_object_or_404(GameSolo, id=game_id)
    questions = request.session.get('game_solo_questions', [])
    current_question = questions[game.questions_answered] if game.questions_answered < len(questions) else None

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
            
            game.questions_answered += 1
            game.save()

            if game.questions_answered < 10:
                return redirect('game_solo_detail', game_id=game.id)
            else:
                game.end_time = timezone.now()
                game.save()
                return redirect('game_solo_summary', game_id=game.id)

    return render(request, 'games/game_solo.html', {'game': game, 'question': current_question})


@login_required
def create_game_random(request, game_mode):
    opponent = User.objects.filter().exclude(id=request.user.id).order_by('?').first()
    if opponent:
        game = GameRandom.objects.create(player1=request.user, player2=opponent, game_mode=game_mode)
        return redirect('game_random_detail', game_id=game.id)
    return render(request, 'games/game_random.html', {'error': 'No opponents available'})

@login_required
def game_random_detail(request, game_id):
    game = get_object_or_404(GameRandom, id=game_id)
    question = get_random_question(game.game_mode)
    
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if check_answer(question, answer):
            game.score_player1 += 1
            game.save()
            return redirect('game_random_detail', game_id=game.id)
    
    return render(request, 'games/game_random.html', {'game': game, 'question': question})

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
    question = get_random_question(game.game_mode)
    
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if check_answer(question, answer):
            game.score_player1 += 1
            game.save()
            return redirect('game_search_detail', game_id=game.id)
    
    return render(request, 'games/game_search.html', {'game': game, 'question': question})

@login_required
def game_solo_summary(request, game_id):
    game = get_object_or_404(GameSolo, id=game_id)
    return render(request, 'games/game_solo_summary.html', {'game': game})

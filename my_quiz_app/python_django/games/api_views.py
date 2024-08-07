import random
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import GameSolo, GameRandom
from .serializers import GameSoloSerializer, GameRandomSerializer
from .questions import get_random_question, check_answer, load_questions, generate_question
from my_quiz_app.python_django.profiles.models import UserProfile

logger = logging.getLogger(__name__)

class GameSoloViewSet(viewsets.ModelViewSet):
    queryset = GameSolo.objects.all()
    serializer_class = GameSoloSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_game(self, request):
        game_mode = request.data.get('game_mode')
        game = GameSolo.objects.create(player1=request.user, game_mode=game_mode)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.solo_games_played += 1
        profile.save()

        if game_mode in ['mode1', 'mode2']:
            questions = load_questions(game_mode)
            random_questions = [generate_question(random.choice(questions), random.randint(0, 9), game_mode) for _ in range(10)]
        elif game_mode == 'mode3':
            random_questions = [get_random_question(random.choice(['mode1', 'mode2'])) for _ in range(10)]
        else:
            return Response({"error": "Invalid game mode"}, status=status.HTTP_400_BAD_REQUEST)

        game.questions = random_questions
        game.save()

        return Response(GameSoloSerializer(game).data)

    @action(detail=True, methods=['post'])
    def answer_question(self, request, pk=None):
        game = self.get_object()
        questions = game.questions
        current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None

        if not current_question:
            return Response({"error": "No more questions"}, status=status.HTTP_400_BAD_REQUEST)

        answer = request.data.get('answer')
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

        if game.questions_answered_player1 >= 10:
            game.end_time = timezone.now()
            game.save()

            profile = request.user.userprofile
            if game.game_mode == 'mode1':
                profile.solo_points_mode1 += game.score_player1
            elif game.game_mode == 'mode2':
                profile.solo_points_mode2 += game.score_player1
            elif game.game_mode == 'mode3':
                profile.solo_points_mode3 += game.score_player1
            profile.save()

            return Response({"message": "Game over", "score": game.score_player1})

        return Response(GameSoloSerializer(game).data)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        game = self.get_object()
        return Response(GameSoloSerializer(game).data)

class GameRandomViewSet(viewsets.ModelViewSet):
    queryset = GameRandom.objects.all()
    serializer_class = GameRandomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_game(self, request):
        game_mode = request.data.get('game_mode')
        existing_game = GameRandom.objects.filter(player2__isnull=True, game_mode=game_mode).exclude(player1=request.user).first()

        if existing_game:
            existing_game.player2 = request.user
            existing_game.save()
            if not existing_game.questions:
                questions = [get_random_question(game_mode) for _ in range(10)]
                existing_game.questions = questions
                existing_game.save()
            return Response({"redirect_url": f'/games/random/detail/{existing_game.id}/'})
        else:
            game = GameRandom.objects.create(player1=request.user, game_mode=game_mode)
            questions = [get_random_question(game_mode) for _ in range(10)]
            game.questions = questions
            game.save()
            return Response({"message": "Waiting for an opponent...", "game_id": game.id})

    @action(detail=True, methods=['post'])
    def answer_question(self, request, pk=None):
        game = self.get_object()
        questions = game.questions
        if request.user == game.player1:
            current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None
        else:
            current_question = questions[game.questions_answered_player2] if game.questions_answered_player2 < len(questions) else None

        if not current_question:
            return Response({"error": "No more questions"}, status=status.HTTP_400_BAD_REQUEST)

        answer = request.data.get('answer')
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
            if is_correct:
                game.score_player1 += 1
        else:
            game.questions_answered_player2 += 1
            if is_correct:
                game.score_player2 += 1

        game.questions.append(question_data)
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
            return Response({"message": "Game over", "score_player1": game.score_player1, "score_player2": game.score_player2})

        return Response(GameRandomSerializer(game).data)

    @action(detail=True, methods=['post'])
    def cancel_game(self, request, pk=None):
        game = self.get_object()
        if game.player1 == request.user and game.player2 is None:
            game.delete()
            return Response({"message": "Game canceled"})
        return Response({"message": "Cannot cancel the game"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        game = self.get_object()
        result = None
        game_mode = game.game_mode

        profile1 = UserProfile.objects.get(user=game.player1)
        profile2 = UserProfile.objects.get(user=game.player2)

        logger.debug(f"Game {game.id} summary: Player1: {game.player1.username}, Player2: {game.player2.username}")
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

        return Response({
            'game': GameRandomSerializer(game).data,
            'result': result,
            'player1_questions': player1_questions,
            'player2_questions': player2_questions,
        })

import random
import logging
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import GameSolo, GameRandom
from .questions import get_random_question, check_answer, load_questions, generate_question
from .serializers import GameSoloSerializer, GameRandomSerializer
from my_quiz_app.python_django.profiles.models import UserProfile

logger = logging.getLogger(__name__)

class GameSoloViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, game_mode=None):
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

        request.session['game_solo_questions'] = random_questions
        logger.debug(f"Generated Questions for Solo Game: {random_questions}")

        return Response({"game_id": game.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        game = get_object_or_404(GameSolo, id=pk)
        questions = request.session.get('game_solo_questions', [])
        current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None

        return Response({
            "game": GameSoloSerializer(game).data,
            "question": current_question
        })

    def update(self, request, pk=None):
        game = get_object_or_404(GameSolo, id=pk)
        questions = request.session.get('game_solo_questions', [])
        current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None

        answer = request.data.get('answer')
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

                return Response({"message": "Game completed", "game_id": game.id}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Answer recorded", "question": questions[game.questions_answered_player1]})
        
        return Response({"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST)

class GameRandomViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, game_mode=None):
        existing_game = GameRandom.objects.filter(player2__isnull=True, game_mode=game_mode).exclude(player1=request.user).first()

        if existing_game:
            existing_game.player2 = request.user
            existing_game.save()

            if not existing_game.questions:
                questions = [get_random_question(game_mode) for _ in range(10)]
                existing_game.questions = questions
                existing_game.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'game_{existing_game.id}',
                {
                    'type': 'game_message',
                    'message': 'opponent_joined'
                }
            )
            return Response({"redirect_url": f'/api/games/random/{existing_game.id}/'}, status=status.HTTP_200_OK)
        else:
            game = GameRandom.objects.create(player1=request.user, game_mode=game_mode)
            questions = [get_random_question(game_mode) for _ in range(10)]
            game.questions = questions
            game.save()
            return Response({"message": "Waiting for an opponent...", "game_id": game.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        game = get_object_or_404(GameRandom, id=pk)

        if request.user not in [game.player1, game.player2]:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        if game.player2 is None:
            return Response({"message": "Waiting for an opponent..."}, status=status.HTTP_200_OK)

        questions = game.questions

        if request.user == game.player1:
            current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None
        else:
            current_question = questions[game.questions_answered_player2] if game.questions_answered_player2 < len(questions) else None

        return Response({
            "game": GameRandomSerializer(game).data,
            "question": current_question
        })

    def update(self, request, pk=None):
        game = get_object_or_404(GameRandom, id=pk)

        if request.user not in [game.player1, game.player2]:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        questions = game.questions
        if request.user == game.player1:
            current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None
        else:
            current_question = questions[game.questions_answered_player2] if game.questions_answered_player2 < len(questions) else None

        answer = request.data.get('answer')
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
                return Response({"message": "Game ended", "game_id": game.id}, status=status.HTTP_200_OK)

            if (request.user == game.player1 and game.questions_answered_player1 >= 10) or (request.user == game.player2 and game.questions_answered_player2 >= 10):
                return Response({"message": "Waiting for the other player..."}, status=status.HTTP_200_OK)

            return Response({"message": "Answer recorded", "game_id": game.id}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        game = get_object_or_404(GameRandom, id=pk)
        if game.player1 == request.user and game.player2 is None:
            game.delete()
            return Response({"message": "Game canceled"}, status=status.HTTP_200_OK)
        return Response({"error": "Cannot cancel the game"}, status=status.HTTP_400_BAD_REQUEST)

class GameSummaryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None, game_type=None):
        if game_type == 'solo':
            game = get_object_or_404(GameSolo, id=pk)
        elif game_type == 'random':
            game = get_object_or_404(GameRandom, id=pk)
        else:
            return Response({"error": "Invalid game type"}, status=status.HTTP_400_BAD_REQUEST)

        result = None
        game_mode = game.game_mode

        if game_type == 'random':
            profile1 = UserProfile.objects.get(user=game.player1)
            profile2 = UserProfile.objects.get(user=game.player2)

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

            profile1.save()
            profile2.save()

            game.points_updated = True

        return Response({
            "game": GameRandomSerializer(game).data if game_type == 'random' else GameSoloSerializer(game).data,
            "result": result,
        })


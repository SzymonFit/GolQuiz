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

    def create(self, request):
        logger.debug(f"Request headers: {request.headers}")
        logger.debug(f"CSRF token from request: {request.META.get('HTTP_X_CSRFTOKEN')}")
        logger.debug(f"Session ID from request: {request.session.session_key}")

        game_mode = request.data.get('game_mode')
        if not game_mode:
            return Response({"error": "game_mode is required"}, status=status.HTTP_400_BAD_REQUEST)

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

        logger.debug(f"Generated Questions for Solo Game: {random_questions}")

        return Response({"game_id": game.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        game = get_object_or_404(GameSolo, id=pk)

        logger.debug(f"Request headers: {request.headers}")
        logger.debug(f"CSRF token from request: {request.META.get('HTTP_X_CSRFTOKEN')}")
        logger.debug(f"Session ID from request: {request.session.session_key}")

        logger.debug(f"Request user: {request.user}, Game player1: {game.player1}")

        if request.user != game.player1:
            logger.warning(f"Unauthorized access attempt by {request.user} for game {pk}")
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        logger.info(f"Authorized access by {request.user} for game {pk}")
        return Response({
            "game": GameSoloSerializer(game).data,
            "questions": game.questions
        })

    def update(self, request, pk=None):
        game = get_object_or_404(GameSolo, id=pk)
        questions = game.questions
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
            if game.questions_answered_player1 >= 10:
                return Response({"message": "Czekaj na zakończenie przez drugiego gracza."}, status=status.HTTP_200_OK)
            
            current_question = questions[game.questions_answered_player1] if game.questions_answered_player1 < len(questions) else None
        else:
            if game.questions_answered_player2 >= 10:
                return Response({"message": "Czekaj na zakończenie przez drugiego gracza."}, status=status.HTTP_200_OK)
            
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

                # Zakończenie gry bez aktualizacji profili (zostanie to zrobione w summary)
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
                return Response({"message": "Czekaj na zakończenie przez drugiego gracza."}, status=status.HTTP_200_OK)

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

        if game_type == 'random':
            # Only check and update points for random games
            if not game.points_updated:
                profile1 = UserProfile.objects.get(user=game.player1)
                profile2 = UserProfile.objects.get(user=game.player2)

                # Calculate the result
                if game.score_player1 > game.score_player2:
                    result = f"{game.player1.username} wins!"
                    self._update_profiles(profile1, profile2, game.score_player1, game.score_player2, game.game_mode, 'win')
                elif game.score_player1 < game.score_player2:
                    result = f"{game.player2.username} wins!"
                    self._update_profiles(profile2, profile1, game.score_player2, game.score_player1, game.game_mode, 'win')
                else:
                    result = "It's a tie!"
                    self._update_profiles(profile1, profile2, game.score_player1, game.score_player2, game.game_mode, 'tie')

                profile1.save()
                profile2.save()

                # Save the result and mark the game as updated
                game.result = result
                game.points_updated = True
                game.save()
            else:
                result = game.result
        else:
            # For solo games, just return the score and end time, no result calculation needed
            result = None

        game_data = GameRandomSerializer(game).data if game_type == 'random' else GameSoloSerializer(game).data
        
        # Add result between end_time and points_updated if available
        game_data_with_result = {
            "id": game_data["id"],
            "player1": game_data["player1"],
            "player2": game_data.get("player2"),  # player2 may not exist in solo games
            "score_player1": game_data["score_player1"],
            "score_player2": game_data.get("score_player2"),  # score_player2 may not exist in solo games
            "questions_answered_player1": game_data["questions_answered_player1"],
            "questions_answered_player2": game_data.get("questions_answered_player2"),  # may not exist in solo games
            "game_mode": game_data["game_mode"],
            "questions": game_data["questions"],
            "start_time": game_data["start_time"],
            "end_time": game_data["end_time"],
            "result": result,  # Add result here if applicable
            "points_updated": game_data.get("points_updated", False),  # may not exist in solo games
        }

        return Response({
            "game": game_data_with_result,
        })

    def _update_profiles(self, winner_profile, loser_profile, winner_points, loser_points, game_mode, result):
        if result == 'win':
            if game_mode == 'mode1':
                winner_profile.pvp_wins_mode1 += 1
                winner_profile.pvp_points_mode1 += winner_points
                loser_profile.pvp_losses_mode1 += 1
                loser_profile.pvp_points_mode1 += loser_points
            elif game_mode == 'mode2':
                winner_profile.pvp_wins_mode2 += 1
                winner_profile.pvp_points_mode2 += winner_points
                loser_profile.pvp_losses_mode2 += 1
                loser_profile.pvp_points_mode2 += loser_points
            elif game_mode == 'mode3':
                winner_profile.pvp_wins_mode3 += 1
                winner_profile.pvp_points_mode3 += winner_points
                loser_profile.pvp_losses_mode3 += 1
                loser_profile.pvp_points_mode3 += loser_points
        elif result == 'tie':
            if game_mode == 'mode1':
                winner_profile.pvp_draws_mode1 += 1
                winner_profile.pvp_points_mode1 += winner_points
                loser_profile.pvp_draws_mode1 += 1
                loser_profile.pvp_points_mode1 += loser_points
            elif game_mode == 'mode2':
                winner_profile.pvp_draws_mode2 += 1
                winner_profile.pvp_points_mode2 += winner_points
                loser_profile.pvp_draws_mode2 += 1
                loser_profile.pvp_points_mode2 += loser_points
            elif game_mode == 'mode3':
                winner_profile.pvp_draws_mode3 += 1
                winner_profile.pvp_points_mode3 += winner_points
                loser_profile.pvp_draws_mode3 += 1
                loser_profile.pvp_points_mode3 += loser_points

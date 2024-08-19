import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../game.service';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Subscription, interval } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-game-pvp',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './game-pvp.component.html',
  styleUrls: ['./game-pvp.component.scss']
})
export class GamePvpComponent implements OnInit, OnDestroy {
  game: any;
  question: any;
  answer: string = '';
  showCorrectAnswer: boolean = false;
  isLastQuestion: boolean = false;
  gameId: number;
  private socket$: WebSocketSubject<any>;
  private timerSubscription: Subscription | null = null;
  timeLeft: number = 10;  // 10 seconds for each question
  waitingMessage: boolean = false;
  showError: boolean = false;
  showWaitMessage = false;;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private router: Router
  ) {
    this.gameId = parseInt(this.route.snapshot.paramMap.get('id')!, 10);
    this.socket$ = webSocket(`ws://localhost:8000/ws/game/${this.gameId}/`);

  }

  ngOnInit() {
    this.socket$.subscribe((message) => this.handleSocketMessage(message));
    this.loadGameDetails();
  }

  ngOnDestroy() {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
    this.socket$.complete();
  }

  private getCsrfTokenFromCookie(): string | null {
    const name = 'csrftoken=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i].trim();
      if (c.indexOf(name) === 0) {
        return c.substring(name.length, c.length);
      }
    }
    return null;
  }

  // Nagłówki do żądań związanych z grą (z ID sesji)
  getGameHeaders(): HttpHeaders {
    const csrfToken = this.getCsrfTokenFromCookie();
    // Logowanie wartości CSRF Tokena i Session ID
    console.log('CSRF Token:', csrfToken);

    let headers = new HttpHeaders().set('X-CSRFToken', csrfToken || '');
    return headers;
  }

  handleSocketMessage(message: any) {
    console.log('Received WebSocket message:', message); // Logowanie wiadomości WebSocket
  
    if (message.message === 'opponent_joined') {
      this.waitingMessage = false;
      this.loadGameDetails();
    } else if (message.message === 'game_ended') {
      this.finishGame();
    }
  }

  loadGameDetails() {
    this.gameService.getPvpGameDetails(this.gameId).subscribe(data => {
      this.game = data.game;
      this.question = data.question;
      this.isLastQuestion = this.game.questions_answered_player1 >= 9;
      if (this.question) {
        this.startTimer();
      }
    });
  }

  startTimer() {
    this.timeLeft = 10;
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
    this.timerSubscription = interval(1000).subscribe(() => {
      this.timeLeft--;
      if (this.timeLeft === 0) {
        this.submitAnswer('');  // Submit empty answer if time runs out
      }
    });
  }

  submitAnswer(answer: string) {
    if (!this.answer) {
      this.showError = true;  // Wyświetl komunikat o błędzie, jeśli odpowiedź nie jest podana
      return;
    }
  
    const headers = this.getGameHeaders(); // Użycie nagłówków specyficznych dla gry
  
    this.gameService.updateRandomGame(this.gameId, this.answer).subscribe((data: any) => {
      this.showCorrectAnswer = true;
      this.showError = false;  // Ukryj komunikat o błędzie
      this.answer = '';  // Resetowanie odpowiedzi
  
      if (data.message === 'Game ended') {
        this.router.navigate([`/game-summary/${this.gameId}`]); // Przeniesienie na stronę podsumowania dla PvP
      } else if (data.message === 'Czekaj na zakończenie przez drugiego gracza.') {
        this.showWaitMessage = true;  // Wyświetl komunikat o oczekiwaniu na drugiego gracza
      } else {
        this.nextQuestion();
      }
    }, error => {
      console.error("Error submitting answer:", error);
    });
  }
  

  nextQuestion() {
    this.showCorrectAnswer = false;
    this.loadGameDetails();
  }

  finishGame() {
    this.router.navigate([`/game-pvp-summary/${this.gameId}`]);
  }

  // Nowa funkcja do anulowania oczekiwania
  cancelWaiting() {
    if (this.gameId) {
      const headers = this.getGameHeaders();

      this.gameService.cancelRandomGame(this.gameId).subscribe((data: any) => {
        alert(data.message);
        this.router.navigate(['/menu']);  // Powrót do menu po anulowaniu gry
      }, error => {
        console.error("Error during game cancellation:", error);
      });
    } else {
      this.router.navigate(['/menu']);
    }
  }
}

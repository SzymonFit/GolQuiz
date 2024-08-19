import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common'; 
import { RouterModule } from '@angular/router'; 
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
  standalone: true,
  imports: [CommonModule, RouterModule] 
})
export class MenuComponent {
  currentGameMode: string | null = null;
  waitingForOpponent: boolean = false;
  currentGameId: string | null = null;
  questions: any[] = [];

  constructor(private http: HttpClient, private router: Router) {}

  openGameModal(gameMode: string) {
    this.currentGameMode = gameMode;
  }

  closeModal() {
    this.currentGameMode = null;
    this.waitingForOpponent = false;
  }

  startSoloGame(gameMode: string) {
    const headers = this.getHeaders();

    this.http.post(`http://localhost:8000/api/games/solo/`, { game_mode: gameMode }, { headers, withCredentials: true })
      .subscribe((data: any) => {
        this.currentGameId = data.game_id;
        this.fetchQuestions();
        this.router.navigate([`/game-solo/${this.currentGameId}`], { state: { questions: this.questions } });
      }, error => {
        console.error("Error during game creation:", error);
      });
  }

  fetchQuestions() {
    if (this.currentGameId) {
      const headers = this.getHeaders();

      this.http.get(`http://localhost:8000/api/games/solo/${this.currentGameId}/`, { headers, withCredentials: true })
        .subscribe((data: any) => {
          this.questions = data.questions;
          console.log(this.questions);
        }, error => {
          console.error("Error fetching questions:", error);
        });
    }
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

  private getHeaders(): HttpHeaders {
    const csrfToken = this.getCsrfTokenFromCookie();
    return new HttpHeaders().set('X-CSRFToken', csrfToken || '');
  }

  startPvpGame(gameMode: string) {
    console.log("Rozpoczęcie gry PvP w trybie:", gameMode);
    this.waitingForOpponent = true;
    const headers = this.getHeaders();

    this.http.get(`http://localhost:8000/api/games/random/join/${gameMode}/`, { headers, withCredentials: true })
      .subscribe((data: any) => {
        console.log("Otrzymane dane z backendu (PvP Game):", data);
        
        if (data.redirect_url) {
          console.log("Otrzymany redirect_url:", data.redirect_url);
          
          // Jeśli URL zawiera `/api/games/random/`, wyciągamy `game_id`
          if (data.redirect_url.startsWith('/api/games/random/')) {
            const match = data.redirect_url.match(/\/api\/games\/random\/(\d+)/);
            if (match) {
              this.currentGameId = match[1];
              console.log("Otrzymane game_id:", this.currentGameId);
              this.router.navigate([`/game-pvp/${this.currentGameId}`]);
            }
          } else {
            window.location.href = data.redirect_url;
          }
        } else if (data.game_id) {
          console.log("Otrzymane game_id:", data.game_id);
          this.currentGameId = data.game_id; 
          const socket$ = this.openWebSocket(data.game_id);
          socket$.subscribe((message: any) => {
            console.log("Otrzymano wiadomość WebSocket:", message);
            if (message.message === 'opponent_joined') {
              console.log("Przekierowanie na:", `/game-pvp/${this.currentGameId}`);``
              this.router.navigate([`/game-pvp/${this.currentGameId}`]);
            }
          });
        } else if (data.message) {
          alert(data.message);
        }
      }, error => {
        console.error("Error during PvP game creation:", error);
      });
  }

  
  
  cancelWaiting() {
    if (this.currentGameId) {
      const headers = this.getHeaders();
  
      this.http.delete(`http://localhost:8000/api/games/random/cancel/${this.currentGameId}/`, { headers, withCredentials: true })
        .subscribe((data: any) => {
          alert(data.message);
          this.closeModal();
          this.currentGameId = null;
        }, error => {
          console.error("Error during game cancellation:", error);
        });
    } else {
      this.closeModal();
    }
  }
  

  private openWebSocket(gameId: string): WebSocketSubject<any> {
    // Użyj poprawnego URL WebSocket z poprawnym portem
    const url = `ws://localhost:8000/ws/game/${gameId}/`;
    return webSocket(url);
  }

  goToProfile() {
    this.router.navigate(['/profile']);
  }

  goToRanking(gameMode: string) {
    this.router.navigate([`/ranking/${gameMode}`]);
  }
}

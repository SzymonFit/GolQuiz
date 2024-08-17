import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';
import { CommonModule } from '@angular/common'; 
import { RouterModule } from '@angular/router'; 

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

  constructor(private http: HttpClient, private router: Router) {}

  openGameModal(gameMode: string) {
    this.currentGameMode = gameMode;
  }

  closeModal() {
    this.currentGameMode = null;
    this.waitingForOpponent = false;
  }

  startSoloGame(gameMode: string) {
    this.router.navigate([`/game-solo/${gameMode}`]);
  }

  startPvpGame(gameMode: string) {
    this.waitingForOpponent = true;
    this.http.get(`/api/games/random/join/${gameMode}/`).subscribe((data: any) => {
      if (data.redirect_url) {
        this.router.navigateByUrl(data.redirect_url);
      } else if (data.game_id) {
        this.currentGameId = data.game_id;
        const socket$ = this.openWebSocket(data.game_id);
        socket$.subscribe((message: any) => {
          if (message.message === 'opponent_joined') {
            this.router.navigate([`/game-pvp/${this.currentGameId}`]);
          }
        });
      } else if (data.message) {
        alert(data.message);
      }
    });
  }

  cancelWaiting() {
    if (this.currentGameId) {
      this.http.get(`/api/games/random/cancel/${this.currentGameId}/`).subscribe((data: any) => {
        alert(data.message);
        this.closeModal();
        this.currentGameId = null;
      });
    } else {
      this.closeModal();
    }
  }

  private openWebSocket(gameId: string): WebSocketSubject<any> {
    const url = `ws://${window.location.host}/ws/game/${gameId}/`;
    return webSocket(url);
  }

  goToProfile() {
    this.router.navigate(['/profile']);
  }

  goToRanking(gameMode: string) {
    this.router.navigate([`/ranking/${gameMode}`]); // Przekierowanie na stronę rankingu
  }
}

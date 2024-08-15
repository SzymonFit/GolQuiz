import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../game.service';
import { WebSocketSubject } from 'rxjs/webSocket';

@Component({
  selector: 'app-game-pvp',
  templateUrl: './game-pvp.component.html',
  styleUrls: ['./game-pvp.component.scss']
})
export class GamePvpComponent implements OnInit {
  gameMode: string;
  currentGameId: number;
  private socket: WebSocketSubject<any>;

  constructor(private route: ActivatedRoute, private gameService: GameService, private router: Router) {
    this.gameMode = '';
    this.currentGameId = 0;
    this.socket = new WebSocketSubject<any>('ws://${window.location.host}/ws/game/${gameId}/');
  }

  ngOnInit(): void {
    this.gameMode = this.route.snapshot.paramMap.get('mode')!;
    this.searchRandomOpponent();
  }

  searchRandomOpponent() {
    this.gameService.createRandomGame(this.gameMode).subscribe(response => {
      this.currentGameId = response.game_id;
      this.openWebSocket(this.currentGameId);
    });
  }

  openWebSocket(gameId: number) {
    this.socket = new WebSocketSubject(`ws://${window.location.host}/ws/game/${gameId}/`);
    this.socket.subscribe(message => {
      if (message.type === 'opponent_joined') {
        this.router.navigate([`/game-pvp`, gameId]);
      }
    });
  }

  cancelGame() {
    this.gameService.cancelRandomGame(this.currentGameId).subscribe(response => {
      alert(response.message);
      this.socket.unsubscribe();
    });
  }
}

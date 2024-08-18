import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { GameService } from '../game.service';

@Component({
  selector: 'app-game-pvp-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-pvp-summary.component.html',
  styleUrls: ['./game-pvp-summary.component.scss']
})
export class GamePvpSummaryComponent {
  game: any;
  gameId: number;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService
  ) {
    this.gameId = parseInt(this.route.snapshot.paramMap.get('id')!, 10);
    this.loadGameSummary();
  }

  loadGameSummary() {
    this.gameService.getPvpGameSummary(this.gameId).subscribe(data => {
      this.game = data.game;
    });
  }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../game.service';

@Component({
  selector: 'app-game-solo-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-solo-summary.component.html',
  styleUrls: ['./game-solo-summary.component.scss']
})
export class GameSoloSummaryComponent {
  game: any;
  gameId: number;
question: any;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private router: Router
  ) {
    this.gameId = parseInt(this.route.snapshot.paramMap.get('id')!, 10);
    this.loadGameSummary();
  }

  loadGameSummary() {
    this.gameService.getSoloGameSummary(this.gameId).subscribe(data => {
      this.game = data.game;
    });
  }

  goToMenu() {
    this.router.navigate(['/menu']);  // Przekierowanie do menu
  }
}

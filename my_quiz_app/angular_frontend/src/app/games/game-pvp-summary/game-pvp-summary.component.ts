import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
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
  player2Questions: any;
  result: any;
q : any;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private router: Router
  ) {
    this.gameId = parseInt(this.route.snapshot.paramMap.get('id')!, 10);
    this.loadGameSummary();
  }

  loadGameSummary() {
    this.gameService.getPvpGameSummary(this.gameId).subscribe(data => {
      this.game = data.game;
    });
  }
  
  goToMenu(){
    this.router.navigate(['/menu']);
  }
}

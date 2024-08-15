import { Component, OnInit } from '@angular/core';
import { GameService } from '../game.service';

@Component({
  selector: 'app-game-solo-summary',
  templateUrl: './game-solo-summary.component.html',
  styleUrls: ['./game-solo-summary.component.scss']
})
export class GameSoloSummaryComponent implements OnInit {
  summary: any;

  constructor(private gameService: GameService) { }

  ngOnInit(): void {
    const gameId = 1; // Przykładowy ID gry, zmień na dynamiczne
    this.gameService.getSoloGameSummary(gameId).subscribe(data => {
      this.summary = data;
    });
  }
}

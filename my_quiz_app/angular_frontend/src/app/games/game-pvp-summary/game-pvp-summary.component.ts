import { Component, OnInit } from '@angular/core';
import { GameService } from '../game.service';

@Component({
  selector: 'app-game-pvp-summary',
  templateUrl: './game-pvp-summary.component.html',
  styleUrls: ['./game-pvp-summary.component.scss']
})
export class GamePvpSummaryComponent implements OnInit {
  summary: any;

  constructor(private gameService: GameService) { }

  ngOnInit(): void {
    const gameId = 1; // Przykładowy ID gry, zmień na dynamiczne
    this.gameService.getPvpGameSummary(gameId).subscribe(data => {
      this.summary = data;
    });
  }
}

import { Component, OnInit } from '@angular/core';
import { GameService } from '../game.service';

@Component({
  selector: 'app-game-solo',
  templateUrl: './game-solo.component.html',
  styleUrls: ['./game-solo.component.scss']
})
export class GameSoloComponent implements OnInit {
  gameDetails: any;
  currentQuestion: any;

  constructor(private gameService: GameService) { }

  ngOnInit(): void {
    const gameId = 1; // Przykładowy ID gry, zmień na dynamiczne
    this.gameService.getSoloGameDetails(gameId).subscribe(data => {
      this.gameDetails = data.game;
      this.currentQuestion = data.question;
    });
  }

  submitAnswer(answer: string) {
    this.gameService.updateSoloGame(this.gameDetails.id, answer).subscribe(data => {
      this.currentQuestion = data.question;
    });
  }
}

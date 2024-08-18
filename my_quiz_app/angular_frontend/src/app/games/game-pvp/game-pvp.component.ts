import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../game.service';

@Component({
  selector: 'app-game-pvp',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './game-pvp.component.html',
  styleUrls: ['./game-pvp.component.scss']
})
export class GamePvpComponent {
  game: any;
  question: any;
  answer: string = '';
  showCorrectAnswer: boolean = false;
  isLastQuestion: boolean = false;
  gameId: number;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private router: Router
  ) {
    this.gameId = parseInt(this.route.snapshot.paramMap.get('id')!, 10);
    this.loadGameDetails();
  }

  loadGameDetails() {
    this.gameService.getPvpGameDetails(this.gameId).subscribe(data => {
      this.game = data.game;
      this.question = data.question;
      this.isLastQuestion = this.game.questions_answered_player1 >= 9;
    });
  }

  submitAnswer() {
    this.gameService.updateRandomGame(this.gameId, this.answer).subscribe(data => {
      this.showCorrectAnswer = true;
      this.answer = '';
      if (data.message === 'Game ended') {
        this.router.navigate([`/game-pvp-summary/${data.game_id}`]);
      } else {
        this.loadGameDetails();
      }
    });
  }

  nextQuestion() {
    this.showCorrectAnswer = false;
    this.loadGameDetails();
  }

  finishGame() {
    this.router.navigate([`/game-pvp-summary/${this.gameId}`]);
  }
}

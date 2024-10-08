import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../game.service';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-game-solo',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './game-solo.component.html',
  styleUrls: ['./game-solo.component.scss']
})
export class GameSoloComponent implements OnInit {
  game: any;
  questions: any[] = [];
  currentQuestion: any;
  answer: string = "";
  showCorrectAnswer: boolean = false;
  isLastQuestion: boolean = false;
  gameId: number;
  showError: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private router: Router
  ) {
    this.gameId = parseInt(this.route.snapshot.paramMap.get('id')!, 10);
  }

  ngOnInit() {
    this.loadGameDetails();
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

  getGameHeaders(): HttpHeaders {
    const csrfToken = this.getCsrfTokenFromCookie();
    console.log('CSRF Token:', csrfToken);

    let headers = new HttpHeaders().set('X-CSRFToken', csrfToken || '');
    return headers;
}

loadGameDetails() {
  const headers = this.getGameHeaders();
  console.log('Request headers before service call:', headers);

  this.gameService.getSoloGameDetails(this.gameId, { headers, withCredentials: true }).subscribe(data => {
      console.log('Otrzymane dane:', data); 
      this.game = data.game;
      this.questions = data.questions;
      this.currentQuestion = this.questions[0];
      this.isLastQuestion = this.questions.length === 1;
  }, error => {
      console.error("Error loading game details:", error);
      if (error.status === 403) {
          console.error("Błąd 403: Forbidden - problem z uwierzytelnieniem");
      }
  });
}

submitAnswer() {
  if (!this.answer) {
    this.showError = true; 
    return;
  }

  const headers = this.getGameHeaders(); 
  
  this.gameService.updateSoloGame(this.gameId, this.answer).subscribe((data: any) => {  
    this.showCorrectAnswer = true;
    this.showError = false;  
    this.answer = ''; 

    if (data.message === 'Game completed') {
      this.router.navigate([`/game-solo-summary/${data.game_id}`]);
    } else {
      this.nextQuestion();
    }
  }, error => {
    console.error("Error submitting answer:", error);
  });
}

nextQuestion() {
  const currentIndex = this.questions.indexOf(this.currentQuestion);
  if (currentIndex + 1 < this.questions.length) {
    this.currentQuestion = this.questions[currentIndex + 1];
    this.showCorrectAnswer = false;
    this.isLastQuestion = currentIndex + 1 === this.questions.length - 1;
  } else {
    this.finishGame();
  }
}


  finishGame() {
    this.router.navigate([`/game-solo-summary/${this.gameId}`]);
  }
}

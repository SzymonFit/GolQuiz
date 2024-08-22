import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    RouterModule
  ]
})
export class HomeComponent implements OnInit {
  descriptions: string[] = [
    "Goal Hunter - Test your knowledge of who scored how many goals in a specific season or where they ranked in the top scorers' list",
    "Squad Master - No lineup is a mystery to you. You know the positions, numbers, and clubs of the players like the back of your hand",
   "Champion - You’re a master of both disciplines. Challenge yourself in this ultimate mode."
  ];
  currentDescription: string = '';  
  currentIndex: number = 0;

  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.changeDescription();
    setInterval(() => this.changeDescription(), 10000);
  }

  changeDescription() {
    this.currentDescription = this.descriptions[this.currentIndex];
    this.currentIndex = (this.currentIndex + 1) % this.descriptions.length;
  }

  login() {
    this.authService.login(this.username, this.password).subscribe({
      next: (response) => {
        this.router.navigate(['/menu']); // Przekierowanie do menu po poprawnym logowaniu
      },
      error: (error) => {
        this.errorMessage = 'Błędny login lub hasło. Spróbuj ponownie.';
      }
    });
  }
}

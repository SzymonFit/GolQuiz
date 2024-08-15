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
    "Tryb 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Tryb 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Tryb 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."
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

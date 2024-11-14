import { Component } from '@angular/core';
import { AuthService } from '../../auth.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss'],
  standalone: true,
  imports: [FormsModule, CommonModule],
})
export class SignupComponent {
  username: string = '';
  password: string = '';
  email: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    this.authService.signup(this.username, this.password, this.email).subscribe({
      next: (response) => {
        this.router.navigate(['/menu']); // Przekierowanie po rejestracji
      },
      error: (error) => {
        this.errorMessage = 'Registration failed. Please try again.';
      }
    });
  }
}

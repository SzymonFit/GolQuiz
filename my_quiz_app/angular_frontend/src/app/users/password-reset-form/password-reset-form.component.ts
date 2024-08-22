import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../auth.service'; 
import { Router } from '@angular/router';

@Component({
  selector: 'app-password-reset-form',
  templateUrl: './password-reset-form.component.html',
  styleUrls: ['./password-reset-form.component.scss'],
  standalone: true,
  imports: [FormsModule]
})
export class PasswordResetFormComponent {
  email: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    console.log('Sending email:', this.email);
    this.authService.resetPassword(this.email).subscribe({
      next: (response) => {
        console.log('Password reset email sent', response);
        this.router.navigate(['accounts/password/reset/done']);
      },
      error: (error) => {
        console.error('Password reset failed', error);
      }
    });
  }
}

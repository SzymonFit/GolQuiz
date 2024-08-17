import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-password-reset-complete',
  standalone: true,
  templateUrl: './password-reset-complete.component.html',
  styleUrls: ['./password-reset-complete.component.scss']
})
export class PasswordResetCompleteComponent {

  constructor(private router: Router) {}

  navigateToHome() {
    this.router.navigate(['/']);
  }
}

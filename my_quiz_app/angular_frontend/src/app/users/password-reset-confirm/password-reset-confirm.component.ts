import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../auth.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-password-reset-confirm',
  templateUrl: './password-reset-confirm.component.html',
  styleUrls: ['./password-reset-confirm.component.scss'],
  standalone: true,
  imports: [FormsModule]
})
export class PasswordResetConfirmComponent implements OnInit {
  newPassword: string = '';
  uid: string | null = '';
  token: string | null = '';

  constructor(
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.uid = this.route.snapshot.paramMap.get('uid');
    this.token = this.route.snapshot.paramMap.get('token');
  }

  onSubmit(): void {
    if (this.uid && this.token) {
      this.authService.confirmResetPassword(this.uid, this.token, this.newPassword).subscribe({
        next: () => {
          this.router.navigate(['/password/reset/complete']);
        },
        error: (error: any) => {
          console.error('Password reset confirm failed', error);
        }
      });
    }
  }
}

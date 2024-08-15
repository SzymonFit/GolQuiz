import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  standalone: true,
  imports: [
    FormsModule
  ]
})
export class LoginComponent {
  loginData = { username: '', password: '' };

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    this.http.post('/api/login/', this.loginData).subscribe(response => {
      // tutaj logika po zalogowaniu
      this.router.navigate(['/']);
    }, error => {
      // obsługa błędów
      console.error('Login failed', error);
    });
  }
}

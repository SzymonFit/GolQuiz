import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, Observable, tap, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  
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
  
  private getHeaders(): HttpHeaders {
    const csrfToken = this.getCsrfTokenFromCookie();
    return new HttpHeaders().set('X-CSRFToken', csrfToken || '');
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/home/`, { username, password }, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  signup(username: string, password: string, email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/accounts/signup/`, { username, password, email }, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout/`, {}, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  resetPassword(email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/accounts/password/reset/`, { email }, {
      headers: this.getHeaders(),
      withCredentials: true
    }).pipe(
      tap(response => console.log('Response from resetPassword:', response)),
      catchError(error => {
        console.error('Error in resetPassword:', error);
        return throwError(error);
      })
    );
  }


  confirmResetPassword(uid: string, token: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/accounts/reset/${uid}/${token}/`, { new_password: newPassword }, {
      headers: this.getHeaders(),
      withCredentials: true
    });
}

}

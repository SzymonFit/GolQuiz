import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserProfile } from './profile.model';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private apiUrl = 'http://localhost:8000/api/menu/profile';

  constructor(private http: HttpClient) {}

  getProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(this.apiUrl, { withCredentials: true });  // Używamy withCredentials
  }

  logout(): Observable<any> {
    const csrfToken = this.getCsrfToken();  // Załóżmy, że masz metodę do pobierania tokenu CSRF
    return this.http.post('http://localhost:8000/api/accounts/logout/', {}, { 
      headers: { 'X-CSRFToken': csrfToken || '' },
      withCredentials: true 
    });
  }
  
  private getCsrfToken(): string | null {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || null;
  }
  
}

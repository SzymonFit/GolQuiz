import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GameService {

  private apiUrl = 'http://localhost:8000/api/games/';

  constructor(private http: HttpClient) { }

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
  private getSessionIdFromCookie(): string | null {
    const name = 'sessionid=';
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
    const sessionId = this.getSessionIdFromCookie();
    let headers = new HttpHeaders().set('X-CSRFToken', csrfToken || '');
    
    if (sessionId) {
      headers = headers.set('Cookie', `sessionid=${sessionId}`);
    }
  
    return headers;
  }

getSoloGameDetails(gameId: number, options?: { headers?: HttpHeaders, withCredentials?: boolean }): Observable<any> {
  const csrfToken = this.getCsrfTokenFromCookie();
  const sessionId = this.getSessionIdFromCookie();
  let headers = new HttpHeaders().set('X-CSRFToken', csrfToken || '');

  if (sessionId) {
      headers = headers.set('Authorization', `Session ${sessionId}`);
  }

  const defaultOptions = {
      headers: headers,
      withCredentials: true // Pozwala na automatyczne przesyłanie cookie
  };

  const finalOptions = { ...defaultOptions, ...options };

  // Logowanie finalnych opcji
  console.log('Final Options in getSoloGameDetails:', finalOptions);

  return this.http.get(`${this.apiUrl}solo/${gameId}/`, finalOptions);
}


  updateSoloGame(gameId: number, answer: string): Observable<any> {
    return this.http.put(`${this.apiUrl}solo/${gameId}/`, { answer }, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  getSoloGameSummary(gameId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}summary/solo/${gameId}/`, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  createRandomGame(gameMode: string): Observable<any> {
    return this.http.post(`${this.apiUrl}random/`, { game_mode: gameMode }, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  getPvpGameDetails(gameId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}random/${gameId}/`, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  updateRandomGame(gameId: number, answer: string): Observable<any> {
    return this.http.put(`${this.apiUrl}random/${gameId}/`, { answer }, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }

  cancelRandomGame(gameId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}random/cancel/${gameId}/`, {
      headers: this.getHeaders(),
      withCredentials: true
    });
  }
  
  getPvpGameSummary(gameId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}summary/random/${gameId}/`, {
      headers: this.getHeaders(),
      withCredentials: true 
    });
  }
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GameService {

  private apiUrl = 'http://127.0.0.1:8000/api/games/';

  constructor(private http: HttpClient) { }

  // Solo Game Methods
  createSoloGame(gameMode: string): Observable<any> {
    return this.http.post(`${this.apiUrl}solo/`, { game_mode: gameMode });
  }

  getSoloGameDetails(gameId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}solo/${gameId}/`);
  }

  updateSoloGame(gameId: number, answer: string): Observable<any> {
    return this.http.put(`${this.apiUrl}solo/${gameId}/`, { answer });
  }

  getSoloGameSummary(gameId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}summary/solo/${gameId}/`);
  }

  // PvP Game Methods
  createRandomGame(gameMode: string): Observable<any> {
    return this.http.post(`${this.apiUrl}random/`, { game_mode: gameMode });
  }

  getPvpGameDetails(gameId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}random/${gameId}/`);
  }

  updateRandomGame(gameId: number, answer: string): Observable<any> {
    return this.http.put(`${this.apiUrl}random/${gameId}/`, { answer });
  }

  cancelRandomGame(gameId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}random/${gameId}/`);
  }

  getPvpGameSummary(gameId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}summary/random/${gameId}/`);
  }
}
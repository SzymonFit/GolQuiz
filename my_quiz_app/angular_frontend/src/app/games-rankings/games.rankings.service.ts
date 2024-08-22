import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GamesRankingsService {
  private apiUrl = 'http://localhost:8000/api/ranking';

  constructor(private http: HttpClient, private router: Router) {
    
  }

  getRankings(gameMode: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/${gameMode}/`, { withCredentials: true });
  }

  goToMenu(){
    this.router.navigate(['/menu']);
  }
}

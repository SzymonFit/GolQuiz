import { Component, OnInit } from '@angular/core';
import { GamesRankingsService } from './games.rankings.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-games-rankings-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './games-rankings-list.component.html',
  styleUrls: ['./games-rankings-list.component.scss']
})
export class GamesRankingsListComponent implements OnInit {

  rankings: any[] = [];
  filteredRankings: any[] = [];
  userPosition: number | null = null;
  gameMode: string = '';
  searchText: string = '';

  constructor(
    private rankingsService: GamesRankingsService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.gameMode = params.get('mode')!;
      this.loadRankings();
    });
  }

  loadRankings(): void {
    this.rankingsService.getRankings(this.gameMode).subscribe({
      next: (data) => {
        this.rankings = data.users;
        this.filteredRankings = this.rankings.slice();
        this.userPosition = data.user_position; 
      },
      error: (err) => console.error('Failed to load rankings', err)
    });
    
  }


  filterRankings(): void {
    if (!this.rankings || this.rankings.length === 0) {
      return; 
    }
  
    if (this.searchText) {
      this.filteredRankings = this.rankings.filter(user =>
        user.username.toLowerCase().includes(this.searchText.toLowerCase())
      );
    } else {
      this.filteredRankings = this.rankings.slice(); 
    }
  }
  
  goToMenu(){
    this.router.navigate(['/menu']);
  }
}


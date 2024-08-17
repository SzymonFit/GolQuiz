import { Component, OnInit } from '@angular/core';
import { RankingsService } from '../rankings.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-ranking-list',
  templateUrl: './ranking-list.component.html',
  styleUrls: ['./ranking-list.component.scss']
})
export class RankingListComponent implements OnInit {
  rankings: any[] = [];  // Po prostu tablica obiektów
  gameMode: string = '';

  constructor(
    private rankingsService: RankingsService,
    private route: ActivatedRoute
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
        this.rankings = data;  // Przypisanie całej odpowiedzi bezpośrednio do rankings
      },
      error: (err) => console.error('Failed to load rankings', err)
    });
  }
}

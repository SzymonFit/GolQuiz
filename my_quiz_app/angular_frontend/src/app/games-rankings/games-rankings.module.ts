import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GamesRankingsRoutingModule } from './games-rankings-routing.module';
import { GamesRankingsListComponent } from './games-rankings-list.component';

@NgModule({
  imports: [
    CommonModule,
    GamesRankingsRoutingModule,
    GamesRankingsListComponent
  ],
  exports: [GamesRankingsListComponent]
  
})
export class GamesRankingsModule { }

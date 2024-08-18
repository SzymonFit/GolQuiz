import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GamePvpComponent } from './game-pvp/game-pvp.component';
import { GamePvpSummaryComponent } from './game-pvp-summary/game-pvp-summary.component';
import { GameSoloComponent } from './game-solo/game-solo.component';
import { GameSoloSummaryComponent } from './game-solo-summary/game-solo-summary.component';

const routes: Routes = [
  { path: 'game-pvp/:id', component: GamePvpComponent },
  { path: 'game-pvp-summary/:id', component: GamePvpSummaryComponent },
  { path: 'game-solo/:id', component: GameSoloComponent },
  { path: 'game-solo-summary/:id', component: GameSoloSummaryComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GamesRoutingModule { }

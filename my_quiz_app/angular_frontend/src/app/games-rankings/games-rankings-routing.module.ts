import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GamesRankingsListComponent } from './games-rankings-list.component';

const routes: Routes = [
  { path: ':mode', component: GamesRankingsListComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GamesRankingsRoutingModule { }

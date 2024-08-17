import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RankingListComponent } from './ranking-list/ranking-list.component';

const routes: Routes = [
  { path: ':mode', component: RankingListComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RankingsRoutingModule { }

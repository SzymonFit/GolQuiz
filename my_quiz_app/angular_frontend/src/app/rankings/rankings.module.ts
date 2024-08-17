import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { RankingsRoutingModule } from './rankings-routing.module';
import { RankingListComponent } from './ranking-list/ranking-list.component';



@NgModule({
  declarations: [RankingListComponent],
  imports: [
    BrowserModule,
    CommonModule,
    RankingsRoutingModule
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RankingsModule { }

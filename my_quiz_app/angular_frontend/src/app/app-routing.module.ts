import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { CsrfInterceptor } from './csrf-interceptor';

import { HomeComponent } from './home/home.component';
import { GamePvpComponent } from './games/game-pvp/game-pvp.component';
import { GameSoloComponent } from './games/game-solo/game-solo.component';
import { GamePvpSummaryComponent } from './games/game-pvp-summary/game-pvp-summary.component';
import { GameSoloSummaryComponent } from './games/game-solo-summary/game-solo-summary.component';
import { MenuComponent } from './menu/menu.component';
import { SignupComponent } from './users/signup/signup.component';
import { PasswordResetFormComponent } from './users/password-reset-form/password-reset-form.component';
import { PasswordResetDoneComponent } from './users/password-reset-done/password-reset-done.component';
import { PasswordResetConfirmComponent } from './users/password-reset-confirm/password-reset-confirm.component';
import { PasswordResetCompleteComponent } from './users/password-reset-complete/password-reset-complete.component';
import { ProfileComponent } from './profiles/profile.component';
import { GamesRankingsListComponent } from './games-rankings/games-rankings-list.component';



export const routes: Routes = [
  { path: '', component: HomeComponent }, // Strona startowa
  { path: 'menu', component: MenuComponent },
  { path: 'game-pvp/:id', component: GamePvpComponent },
  { path: 'game-pvp-summary/:id', component: GamePvpSummaryComponent },
  { path: 'game-solo/:id', component: GameSoloComponent },
  { path: 'game-solo-summary/:id', component: GameSoloSummaryComponent },
  { path: 'accounts/signup', component: SignupComponent },
  { path: 'accounts/password/reset', component: PasswordResetFormComponent },
  { path: 'accounts/password/reset/done', component: PasswordResetDoneComponent },
  { path: 'accounts/reset/:uid/:token', component: PasswordResetConfirmComponent },
  { path: 'accounts/password/reset/complete', component: PasswordResetCompleteComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'ranking/:mode', component: GamesRankingsListComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: CsrfInterceptor, multi: true },
  ]
})
export class AppRoutingModule { }

import { Component, OnInit } from '@angular/core';
import { ProfileService } from './profile.service';
import { UserProfile } from './profile.model';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
  standalone: true,
  imports: [CommonModule] 
})
export class ProfileComponent implements OnInit {
  profile: UserProfile | undefined;
  error: string | undefined;

  constructor(private profileService: ProfileService, private router: Router) {} 

  ngOnInit(): void {
    this.profileService.getProfile().subscribe({
      next: (data: UserProfile) => this.profile = data,
      error: () => this.error = 'Failed to load profile'
    });
  }

  logout() {
    this.profileService.logout().subscribe({
      next: () => {
        this.router.navigate(['/']); 
      },
      error: () => {
        this.error = 'Failed to logout';
      }
    });
  }
  
  goToMenu() {
    this.router.navigate(['/menu']);  
  }
}

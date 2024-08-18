import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GamesRankingsListComponent } from './games-rankings-list.component';

describe('GamesRankingsListComponent', () => {
  let component: GamesRankingsListComponent;
  let fixture: ComponentFixture<GamesRankingsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GamesRankingsListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GamesRankingsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

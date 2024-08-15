import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GamePvpSummaryComponent } from './game-pvp-summary.component';

describe('GamePvpSummaryComponent', () => {
  let component: GamePvpSummaryComponent;
  let fixture: ComponentFixture<GamePvpSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GamePvpSummaryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GamePvpSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

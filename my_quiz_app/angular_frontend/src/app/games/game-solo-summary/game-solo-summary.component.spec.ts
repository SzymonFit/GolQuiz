import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameSoloSummaryComponent } from './game-solo-summary.component';

describe('GameSoloSummaryComponent', () => {
  let component: GameSoloSummaryComponent;
  let fixture: ComponentFixture<GameSoloSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GameSoloSummaryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GameSoloSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

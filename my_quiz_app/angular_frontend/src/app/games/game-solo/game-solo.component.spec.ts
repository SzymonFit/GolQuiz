import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameSoloComponent } from './game-solo.component';

describe('GameSoloComponent', () => {
  let component: GameSoloComponent;
  let fixture: ComponentFixture<GameSoloComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GameSoloComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GameSoloComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

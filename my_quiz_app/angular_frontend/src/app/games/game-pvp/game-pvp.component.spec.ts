import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GamePvpComponent } from './game-pvp.component';

describe('GamePvpComponent', () => {
  let component: GamePvpComponent;
  let fixture: ComponentFixture<GamePvpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GamePvpComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GamePvpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

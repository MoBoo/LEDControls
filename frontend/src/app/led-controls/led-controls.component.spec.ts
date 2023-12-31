import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LedControlsComponent } from './led-controls.component';

describe('LedControlsComponent', () => {
  let component: LedControlsComponent;
  let fixture: ComponentFixture<LedControlsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LedControlsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LedControlsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

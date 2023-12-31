import { Component } from '@angular/core';
import { LedControlService } from './services/led-control.service'

@Component({
  selector: 'app-led-controls',
  templateUrl: './led-controls.component.html',
  styleUrl: './led-controls.component.scss'
})
export class LedControlsComponent {
  color: string|undefined = undefined;
  theater_chase_color: string|undefined = undefined;
  brightness: number = 255;
  is_led_on = false;

  constructor(
    private led_controller: LedControlService
  ) { }

  set_led_color(color: string) {
    this.led_controller.set_pattern('solid', color).subscribe({
      next: () => {
        this.is_led_on = color !== '#000000';
      }
    });
  }

  set_led_brightness(value: number) {
    this.led_controller.set_brightness(value).subscribe();
  }

  set_led_pattern(pattern: string, color?: string) {
    this.led_controller.set_pattern(pattern, color).subscribe({
      next: () => {
        this.is_led_on = true;
      }
    });
  }
}

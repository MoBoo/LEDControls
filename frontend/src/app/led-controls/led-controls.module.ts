import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgxColorsModule } from 'ngx-colors';
import { LedControlsRoutingModule } from './led-controls-routing.module'
import { LedControlsComponent } from './led-controls.component';


@NgModule({
  declarations: [
    LedControlsComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgxColorsModule,
    LedControlsRoutingModule,
  ]
})
export class LedControlsModule { }

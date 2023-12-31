import { RouterModule, Routes } from '@angular/router';
import { LedControlsComponent } from './led-controls.component';
import { NgModule } from '@angular/core';

const routes: Routes = [
    {
        path: '',
        component: LedControlsComponent
    },
    {
        path: '**',
        redirectTo: ''
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class LedControlsRoutingModule { }

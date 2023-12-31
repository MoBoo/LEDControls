import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LedControlService {
  constructor(
    private http: HttpClient
  ) {}

  set_brightness(value: number): Observable<any> {
    return this.http.post(`${environment.led_api_url}/brightness`, { value })
  }

  set_pattern(pattern: string, color?: string): Observable<any> {
    return this.http.post(`${environment.led_api_url}/pattern`, { pattern, color })
  }
}

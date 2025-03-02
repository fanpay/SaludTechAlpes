import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { Solicitud } from '../core/detail.interface';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ListService {
  private baseURL = `${environment.apiUrl}/solicitudes`;
  private _httpClient: HttpClient = inject(HttpClient);
  private readonly authService: AuthService = inject(AuthService);
  token = this.authService.isAuthenticated();
  username = this.authService.getUsername();

  getListByUser(): Observable<{ state: Solicitud[] }> {
    console.log('Desde el servicio solicitudes: ', this.username);

    const headers = new HttpHeaders({ Authorization: `Bearer ${this.token}` });
    return this._httpClient.get<{ state: Solicitud[] }>(
      `${this.baseURL}/${this.username}`,
      {
        headers,
      }
    );
  }
}

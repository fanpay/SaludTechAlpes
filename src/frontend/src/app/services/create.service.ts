import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';
import { Solicitud } from '../core/solicitud.interface';

@Injectable({
  providedIn: 'root',
})
export class CreateService {
  private baseURL = `${environment.apiUrl}/registro`;
  private _httpClient: HttpClient = inject(HttpClient);
  private readonly authService: AuthService = inject(AuthService);
  token = this.authService.isAuthenticated();
  username = this.authService.getUsername();

  crearSolicitud(nueva_solicitud: Solicitud): Observable<{ state: Solicitud }> {
    console.log('Desde el servicio - nueva solicitud; ', nueva_solicitud)
    const headers = new HttpHeaders({ Authorization: `Bearer ${this.token}` });

    return this._httpClient.post<{ state: Solicitud }>(
      `${this.baseURL}`,
      nueva_solicitud,
      {
        headers,
      }
    );
  }
}

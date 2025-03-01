import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { Detail } from '../core/detail.interface';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DetailService {
  private detailsUrl = `${environment.apiUrl}/anonimizacion`;
  private _httpClient: HttpClient = inject(HttpClient);
  private readonly authService: AuthService = inject(AuthService);
  token = this.authService.isAuthenticated();

  getDetailsById(id: string): Observable<{ state: Detail }> {
    console.log('Desde el servicio details: ', this.token);

    const headers = new HttpHeaders({ Authorization: `Bearer ${this.token}` });
    return this._httpClient.get<{ state: Detail }>(`${this.detailsUrl}/${id}`, {
      headers,
    });
  }
}

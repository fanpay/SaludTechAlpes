import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private loginUrl = `${environment.apiUrl}/auth/authenticate`;
  private _httpClient: HttpClient = inject(HttpClient);
  private tokenKey = 'authToken';
  #authUsername: string = 'authUser' ;

  login(apiKey: string): Observable<any> {
    return this._httpClient
      .post<any>(`${this.loginUrl}?api_key=${apiKey}`, null)
      .pipe(
        tap((response) => {
          if (response.token) {
            this.setToken(response.token);
            this.setUsername(response.user);
          }
        })
      );
  }

  private setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  private setUsername(username: string): void {
    localStorage.setItem(this.#authUsername, username);
  }

  private getToken(): string | null {
    return localStorage ? localStorage.getItem(this.tokenKey) : '';
  }

  public getUsername(): string | null {
    return localStorage ? localStorage.getItem(this.#authUsername) : '';
  }

  isAuthenticated(): string | null {
    const token = this.getToken();

    if (!token) {
      console.error('Ususario no autenticado');
    }

    return token;
  }
}

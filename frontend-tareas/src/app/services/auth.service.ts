import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { LoginRequest, LoginResponse, RegistroRequest, Usuario } from '../models/usuario.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:5001/auth';
  private tokenKey = 'access_token';
  private currentUserSubject = new BehaviorSubject<Usuario | null>(null);
  
  constructor(private http: HttpClient) {
    // Verificar si hay un usuario logueado al inicializar
    this.loadCurrentUser();
  }

  register(data: RegistroRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, data);
  }

  login(data: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, data)
      .pipe(
        tap(response => {
          if (response.access_token) {
            localStorage.setItem(this.tokenKey, response.access_token);
            if (response.usuario) {
              this.currentUserSubject.next(response.usuario);
            }
          }
        })
      );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.currentUserSubject.next(null);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    const token = this.getToken();
    if (!token) return false;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp > Date.now() / 1000;
    } catch {
      return false;
    }
  }

  getCurrentUser(): Observable<Usuario | null> {
    return this.currentUserSubject.asObservable();
  }

  private loadCurrentUser(): void {
    if (this.isLoggedIn()) {
      // Aquí podrías hacer una llamada al backend para obtener los datos del usuario actual
      // Por ahora, simplemente marcamos que hay un usuario logueado
      this.currentUserSubject.next({ id: 1, usuario: 'usuario', email: 'user@example.com' });
    }
  }
}
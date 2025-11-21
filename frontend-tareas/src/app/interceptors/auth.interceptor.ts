import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();
  
  // Siempre agregar Content-Type para peticiones POST/PUT
  let headers: any = {};
  
  if (req.method === 'POST' || req.method === 'PUT') {
    headers['Content-Type'] = 'application/json';
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  if (Object.keys(headers).length > 0) {
    const authReq = req.clone({
      setHeaders: headers
    });
    return next(authReq);
  }
  
  return next(req);
};
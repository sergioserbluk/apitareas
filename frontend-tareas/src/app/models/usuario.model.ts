export interface Usuario {
  id?: number;
  usuario: string;
  email: string;
}

export interface RegistroRequest {
  usuario: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  usuario: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  usuario?: Usuario;
}
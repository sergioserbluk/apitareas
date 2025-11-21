export interface Tarea {
  id?: number;
  titulo: string;
  hecha: boolean;
  usuario_id?: number;
}

export interface TareaRequest {
  titulo: string;
  hecha?: boolean;
}
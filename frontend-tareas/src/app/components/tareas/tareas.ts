import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { TareasService } from '../../services/tareas.service';
import { Tarea, TareaRequest } from '../../models/tarea.model';

@Component({
  selector: 'app-tareas',
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatCheckboxModule,
    MatSnackBarModule,
    MatDialogModule
  ],
  templateUrl: './tareas.html',
  styleUrl: './tareas.css'
})
export class TareasComponent implements OnInit {
  tareas: Tarea[] = [];
  nuevaTarea: TareaRequest = { titulo: '', hecha: false };
  editingTarea: Tarea | null = null;

  constructor(
    private tareasService: TareasService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadTareas();
  }

  loadTareas(): void {
    this.tareasService.getTareas().subscribe({
      next: (tareas) => {
        this.tareas = tareas;
      },
      error: (error) => {
        this.snackBar.open('Error al cargar las tareas', 'Cerrar', { duration: 3000 });
      }
    });
  }

  createTarea(): void {
    if (!this.nuevaTarea.titulo.trim()) {
      this.snackBar.open('El título es requerido', 'Cerrar', { duration: 3000 });
      return;
    }

    this.tareasService.createTarea(this.nuevaTarea).subscribe({
      next: (tarea) => {
        this.tareas.push(tarea);
        this.nuevaTarea = { titulo: '', hecha: false };
        this.snackBar.open('Tarea creada exitosamente', 'Cerrar', { duration: 3000 });
      },
      error: (error) => {
        this.snackBar.open('Error al crear la tarea', 'Cerrar', { duration: 3000 });
      }
    });
  }

  updateTarea(tarea: Tarea): void {
    if (!tarea.id) return;

    const tareaRequest: TareaRequest = {
      titulo: tarea.titulo,
      hecha: tarea.hecha
    };

    this.tareasService.updateTarea(tarea.id, tareaRequest).subscribe({
      next: (updatedTarea) => {
        const index = this.tareas.findIndex(t => t.id === tarea.id);
        if (index !== -1) {
          this.tareas[index] = updatedTarea;
        }
        this.editingTarea = null;
        this.snackBar.open('Tarea actualizada exitosamente', 'Cerrar', { duration: 3000 });
      },
      error: (error) => {
        this.snackBar.open('Error al actualizar la tarea', 'Cerrar', { duration: 3000 });
      }
    });
  }

  deleteTarea(tarea: Tarea): void {
    if (!tarea.id) return;

    if (confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
      this.tareasService.deleteTarea(tarea.id).subscribe({
        next: () => {
          this.tareas = this.tareas.filter(t => t.id !== tarea.id);
          this.snackBar.open('Tarea eliminada exitosamente', 'Cerrar', { duration: 3000 });
        },
        error: (error) => {
          this.snackBar.open('Error al eliminar la tarea', 'Cerrar', { duration: 3000 });
        }
      });
    }
  }

  toggleTareaComplete(tarea: Tarea): void {
    tarea.hecha = !tarea.hecha;
    this.updateTarea(tarea);
  }

  startEdit(tarea: Tarea): void {
    this.editingTarea = { ...tarea };
  }

  cancelEdit(): void {
    this.editingTarea = null;
  }

  saveEdit(): void {
    if (this.editingTarea) {
      this.updateTarea(this.editingTarea);
    }
  }
}

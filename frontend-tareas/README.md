# Frontend Angular - API Tareas

Este es el frontend Angular que consume la API de Tareas desarrollada con Flask-RESTX.

## Configuración Rápida

### 1. Instalar dependencias
```bash
npm install
```

### 2. Ejecutar el servidor de desarrollo
```bash
ng serve
```

### 3. Abrir en el navegador
Navegar a `http://localhost:4200`

## Características

- ✅ **Autenticación JWT**: Login y registro seguro
- ✅ **Gestión de Tareas**: CRUD completo de tareas
- ✅ **Material Design**: Interfaz moderna con Angular Material
- ✅ **Guards de Routing**: Protección de rutas autenticadas
- ✅ **Interceptors HTTP**: Inyección automática de JWT
- ✅ **Responsive Design**: Adaptable a móviles y desktop

## Uso de la Aplicación

### Registro e Inicio de Sesión
1. Ir a `/registro` para crear una cuenta nueva
2. Usar `/login` para iniciar sesión con credenciales existentes

### Gestión de Tareas
1. Crear tareas nuevas con el formulario
2. Marcar tareas como completadas
3. Editar títulos de tareas
4. Eliminar tareas no necesarias

## Estructura Técnica

```
src/app/
├── components/     # Componentes de UI
├── services/       # Servicios de datos
├── models/         # Interfaces TypeScript
├── guards/         # Protección de rutas
└── interceptors/   # Interceptors HTTP
```

## API Integration

El frontend consume la API Flask en:
- **Auth**: `http://127.0.0.1:5000/auth`
- **Tareas**: `http://127.0.0.1:5000/tareas`

## Comandos de Desarrollo

```bash
# Servidor de desarrollo
ng serve

# Build para producción
ng build

# Verificar código
ng lint

# Tests unitarios
ng test
```

## Requisitos

- Node.js 16+
- Angular CLI
- API Backend ejecutándose en puerto 5000
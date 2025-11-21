# Script para ejecutar Backend y Frontend

## Opción 1: Ejecutar ambos en terminales separadas

### Terminal 1 - Backend Flask:
```bash
cd C:\Users\sergi\source\repos\apitareas
python app.py
```

### Terminal 2 - Frontend Angular:
```bash
cd C:\Users\sergi\source\repos\apitareas\frontend-tareas
ng serve
```

## Opción 2: Script PowerShell

Crear archivo `start.ps1`:

```powershell
# Iniciar Backend
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\sergi\source\repos\apitareas'; python app.py"

# Esperar 3 segundos
Start-Sleep 3

# Iniciar Frontend
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\sergi\source\repos\apitareas\frontend-tareas'; ng serve"

# Abrir navegador
Start-Sleep 5
Start-Process "http://localhost:4200"
```

## URLs de la aplicación

- **Frontend**: http://localhost:4200
- **Backend API**: http://127.0.0.1:5000
- **Swagger Docs**: http://127.0.0.1:5000/swagger

## Test de la aplicación

1. **Registro**: Crear usuario en http://localhost:4200/registro
2. **Login**: Iniciar sesión en http://localhost:4200/login  
3. **Tareas**: Gestionar tareas en http://localhost:4200/tareas

## Detener las aplicaciones

- En cada terminal presionar `Ctrl+C`
- O cerrar las ventanas de PowerShell
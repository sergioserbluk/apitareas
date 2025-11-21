# Solución para CORS - API Tareas

## Cambios Realizados

### 1. Backend (app.py) - Configuración CORS mejorada:
```python
CORS(app, 
     origins=['http://localhost:4200', 'http://127.0.0.1:4200'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)
```

### 2. Frontend - Interceptor HTTP actualizado:
- Migrado a la nueva API funcional de Angular 18
- Agregado Content-Type header automáticamente
- Mejor manejo de tokens JWT

### 3. Verificar que funciona:

#### Test con curl:
```bash
# Registro
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"usuario":"test","email":"test@test.com","password":"123"}'

# Login  
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"test","password":"123"}'
```

#### Test desde navegador:
1. Abrir DevTools (F12)
2. Ir a Network tab
3. Intentar login desde el frontend
4. Verificar que no aparecen errores CORS

### 4. URLs de prueba:
- **Frontend**: http://localhost:4200
- **Backend**: http://127.0.0.1:5000
- **API Docs**: http://127.0.0.1:5000/swagger

### 5. Si persiste el problema:

#### Verificar puertos:
```bash
netstat -an | findstr :4200
netstat -an | findstr :5000
```

#### Headers de respuesta esperados:
```
Access-Control-Allow-Origin: http://localhost:4200
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

## Reiniciar aplicaciones:

1. **Backend**: Ctrl+C y ejecutar `python app.py`
2. **Frontend**: Ctrl+C y ejecutar `ng serve`

La configuración CORS ahora permite específicamente las peticiones desde el frontend Angular, incluyendo todos los métodos HTTP necesarios y los headers de autenticación.
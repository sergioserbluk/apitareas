# Nivel 4 — Material complementario práctico (adaptado a esta API)

Este documento es un complemento práctico al material teórico del PDF que proporcionaste. Está escrito específicamente para la API que tienes en este repositorio (archivos: `app.py`, `auth.py`, `routes.py`, `models.py`, `seed.py`, `htmlpruebacors.html`, `utils.py`). Contiene teoría breve, arquitectura, pasos detallados "manos a la obra", ejemplos de requests (PowerShell y curl), ejercicios prácticos y una sección de resolución de problemas (incluye lo que ya corregimos sobre Flask‑RESTX).

---

## 1. Resumen teórico (breve)

- API REST: interfaz HTTP organizada en recursos. Aquí los recursos principales son `tareas` y `usuarios`.
- Autenticación: usamos JWT (JSON Web Tokens) con `flask-jwt-extended`. El flujo es: registro -> login -> obtención del token -> petición con header `Authorization: Bearer <token>`.
- Documentación: `flask-restx` genera Swagger UI desde los `Namespace` y `api.model`.
- Persistencia: `SQLAlchemy` con SQLite por defecto (fichero `database.db`). Los modelos `Usuario` y `Tarea` están en `models.py`.
- CORS: permitimos peticiones desde el frontend de prueba (`htmlpruebacors.html`) usando `flask-cors`.

## 2. Arquitectura de la app (cómo encajan los ficheros)

- `app.py` — app factory: crea `Flask`, registra `Api` (flask-restx) y namespaces, inicializa extensiones (`db`, `jwt`), y expone endpoints base (`/`, `/tareas` público).
- `auth.py` — namespace `auth`: `POST /register`, `POST /login`, `GET /me` (protegido).
- `routes.py` — namespace `tareas`: `GET/POST /api/v1/tareas` y `GET/PUT/DELETE /api/v1/tareas/<id>`.
- `models.py` — `Usuario` (usuario, email, password_hash) y `Tarea` (titulo, hecha, usuario_id).
- `seed.py` — pequeño script para poblar la base de datos (crea usuario demo y algunas tareas).
- `htmlpruebacors.html` — demo frontend para probar llamadas CORS al endpoint público `/tareas`.
- `utils.py` — manejadores de errores y utilidades (p. ej. respuesta 404 personalizada).

## 3. Preparación (setup rápido)

1. Abrir terminal en la carpeta del proyecto:

```powershell
cd C:\Users\sergi\source\repos\apitareas
```

2. (Opcional pero recomendado) Crear y activar virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias (si no lo hiciste aún):

```powershell
pip install -r requirements.txt
```

4. (Opcional) Añadir `.env` con `JWT_SECRET_KEY="cambiar_esto"` u otra clave segura.

5. Poblar datos de ejemplo:

```powershell
python .\seed.py
```

6. Arrancar servidor:

```powershell
python .\app.py
```

- El servidor escucha en `http://127.0.0.1:5000`.
- Swagger UI está disponible en `/swagger` (según la configuración actual de `app.py`). Si ves 404 en `/swagger` revisa que el servidor fue arrancado sin error y que el `Api` fue inicializado correctamente.

## 4. Flujo paso a paso (manos a la obra)

A continuación encontrarás pasos concretos con ejemplos ejecutables para: registro, login, uso del token y operaciones CRUD sobre tareas. Los ejemplos están en PowerShell y en curl.

### 4.1 Registro de usuario

- Endpoint: `POST /api/v1/auth/register`
- Body JSON: `{ "usuario": "alumno", "email": "alumno@example.com", "password": "pass123" }`

PowerShell:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/v1/auth/register' -Method Post -Body (@{ usuario='alumno'; email='alumno@example.com'; password='pass123' } | ConvertTo-Json) -ContentType 'application/json'
```

curl:

```bash
curl -s -X POST "http://127.0.0.1:5000/api/v1/auth/register" -H 'Content-Type: application/json' -d '{"usuario":"alumno","email":"alumno@example.com","password":"pass123"}'
```

Respuesta esperada: 201 con JSON que incluye el `id` del nuevo usuario.

Nota: si ya existe el usuario/email, la API responde 400.

### 4.2 Login y obtención del token JWT

- Endpoint: `POST /api/v1/auth/login`
- Body JSON: `{ "usuario": "alumno", "password": "pass123" }`

PowerShell (guardar token en variable):

```powershell
$resp = Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/v1/auth/login' -Method Post -Body (@{ usuario='alumno'; password='pass123' } | ConvertTo-Json) -ContentType 'application/json'
$token = $resp.token
Write-Host "Token: $token"
```

curl:

```bash
curl -s -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H 'Content-Type: application/json' -d '{"usuario":"alumno","password":"pass123"}'
```

Respuesta: `{ "token": "<JWT>" }`.

### 4.3 Usar el token para llamadas protegidas

- Header: `Authorization: Bearer <token>`

Listar tareas (GET):

PowerShell:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/v1/tareas' -Headers @{ Authorization = "Bearer $token" }
```

curl:

```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://127.0.0.1:5000/api/v1/tareas"
```

Crear tarea (POST):

PowerShell:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/v1/tareas' -Method Post -Body (@{ titulo='Comprar leche'; hecha=$false } | ConvertTo-Json) -ContentType 'application/json' -Headers @{ Authorization = "Bearer $token" }
```

curl:

```bash
curl -s -X POST "http://127.0.0.1:5000/api/v1/tareas" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d '{"titulo":"Comprar leche","hecha":false}'
```

Obtener/Actualizar/Borrar (reemplaza `<id>`):

- `GET /api/v1/tareas/<id>`
- `PUT /api/v1/tareas/<id>` (envía body JSON con campos a actualizar)
- `DELETE /api/v1/tareas/<id>`

### 4.4 Endpoint público (para CORS demo)

- `GET /tareas` — devuelve el contenido de `storage.json`, usado por `htmlpruebacors.html`.
- Abre `htmlpruebacors.html` en el navegador como archivo local o sirviéndolo desde un servidor estático.

## 5. Mapear teoría a tu código (puntos clave)

- ¿Dónde se crea el token? — `auth.py`, función `Login.post` usa `create_access_token(identity=str(u.id))`.
- ¿Dónde se protege un endpoint? — `routes.py`, decorador `@jwt_required()` en métodos de recursos de `flask-restx`.
- ¿Dónde está definido el modelo de tarea? — `routes.py`, `tarea_model = api.model('Tarea', {...})` (para docs) y `models.py` para la estructura real.
- ¿Dónde se registra la documentación? — `app.py` al construir `Api(...)` y registrar `namespaces`.

## 6. Ejercicios prácticos (guiados) — nivel recomendado

Cada ejercicio incluye objetivos, pasos y criterios de aceptación.

### Ejercicio 6.1 — Añadir `descripcion` a `Tarea` (básico)

Objetivo: añadir un campo `descripcion` (texto opcional) a las tareas y exponerlo en la API y docs.

Pasos:
1. Modifica `models.py`: añade columna `descripcion = db.Column(db.String(500), nullable=True)` en la clase `Tarea` y actualiza `to_dict()` para incluirla.
2. Modifica `routes.py`: en `tarea_model` añade `descripcion: fields.String(...)`.
3. Actualiza los endpoints POST/PUT para leer y persistir `descripcion`.
4. Elimina `database.db` (si usas SQLite) y vuelve a ejecutar `python seed.py` para recrear las tablas con la nueva columna.

Criterio de aceptación: crear/obtener tareas con campo `descripcion` y ver el campo en la documentación Swagger.

### Ejercicio 6.2 — Paginación (intermedio)

Objetivo: implementar paginación para `GET /api/v1/tareas` con parámetros `page` y `per_page`.

Pasos:
1. En `routes.py`, en `TareasList.get`, leer `page = int(request.args.get('page', 1))` y `per_page = int(request.args.get('per_page', 10))`.
2. Usar SQLAlchemy `paginate` o `limit/offset` para obtener la página.
3. Devolver estructura `{ items: [...], page: 1, per_page: 10, total: 42 }`.

Criterio: llamadas a `/api/v1/tareas?page=2&per_page=5` devuelven subconjunto correcto y meta datos.

### Ejercicio 6.3 — Validaciones robustas (intermedio)

Objetivo: añadir validaciones en registro y creación de tareas (longitud mínima, tipos correctos).

Pasos:
1. En `auth.py`, validar formato de email mínimo y longitud de password (>= 6).
2. En `routes.py`, validar `titulo` no vacío y `hecha` valor booleano.
3. Usar `api.abort(400, 'mensaje')` o devolver JSON con el error y código 400.

Criterio: entradas inválidas producen 400 con mensaje útil.

### Ejercicio 6.4 — Tests pytest (recomendado)

Objetivo: crear tests básicos para registro, login y CRUD.

Pasos:
1. Añadir carpeta `tests/` con `conftest.py` que proporcione fixtures `app` y `client` (usar SQLite in-memory para rapidez).
2. Escribir tests: `test_register_login.py` y `test_tareas_crud.py`.
3. Ejecutar `pytest -q`.

Criterio: tests básicos pasan (registro -> login -> crear tarea -> listar -> actualizar -> borrar).

## 7. Troubleshooting (problemas vistos y soluciones aplicadas)

- Problema: `KeyError: 'view_class'` al arrancar con `flask-restx`.
  - Causa: mezclar registro directo de rutas en `Api(app)` y `Namespace` con definiciones inconsistentes, o doble registro de la misma ruta/endpoint.
  - Solución aplicada: registrar `Api` correctamente y usar `api.add_namespace(namespace, path='/api/v1/...')`. Evitar usar `Blueprint` junto con `Namespace` si no es necesario.

- Problema: Swagger 404 en `/apidocs/`.
  - Causa frecuente: `Api` no inicializada con la app o `doc` configurado en otra ruta, o `prefix`/`path` que cambia la URL real.
  - Solución aplicada: asegurarse de inicializar `Api(app, doc='/swagger')` o `api.init_app(app)` y comprobar el prefijo global. En este proyecto configuramos Swagger en `/swagger`. Si accedes a `/apidocs` y obtienes 404, prueba `/swagger`.

- Problema: `return` fuera de función / errores de indentación.
  - Causa: restos de código duplicado o conversiones incompletas de Blueprints a Namespaces.
  - Solución: limpiar `auth.py` y `routes.py`, asegurando que todos los endpoints estén dentro de `Resource` y sus métodos.

## 8. Checklist de entrega (rápido)

- [ ] Código funcionando: `python app.py` sin excepciones.
- [ ] Documentación Swagger accesible en `/swagger` (o ruta que configures).
- [ ] Registro y login funcionan (puedes obtener token y usarlo en endpoints protegidos).
- [ ] Seed crea datos de ejemplo y CRUD funciona.
- [ ] Tests mínimos (opcional, recomendado).

## 9. Recursos y siguientes pasos que puedo crear por ti

Puedo generar automáticamente en el repo cualquiera de los siguientes artefactos:

- `tests/` con fixtures y 4–6 tests básicos (registro/login + CRUD).
- `html_demo.html` que implemente un pequeño frontend: registro/login (guarda token en localStorage) y UI para listar/crear/editar/borrar tareas.
- `run.ps1` y `seed.ps1` para Windows PowerShell que automatizan crear el entorno, instalar deps, seed y arrancar la app.

Dime cuál de estos quieres que genere y lo añado directamente al repositorio.

---

Si quieres que adapte todavía más el contenido del PDF (por ejemplo, mantener exactamente el orden y las secciones del PDF), dime las secciones concretas y las adaptaré al código de este repo. También puedo añadir diagramas simples (ASCII o referencias) o un diagrama mermaid si prefieres.

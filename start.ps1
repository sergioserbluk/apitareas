# Iniciar Backend
Write-Host "Iniciando Backend Flask..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-Command", "cd '$PSScriptRoot'; python app.py"

# Esperar a que el backend se inicie
Start-Sleep 3

# Iniciar Frontend
Write-Host "Iniciando Frontend Angular..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-Command", "cd '$PSScriptRoot\frontend-tareas'; ng serve"

# Esperar a que el frontend se compile
Write-Host "Esperando a que Angular compile..." -ForegroundColor Yellow
Start-Sleep 10

# Abrir navegador
Write-Host "Abriendo navegador..." -ForegroundColor Green
Start-Process "http://localhost:4200"

Write-Host "¡Aplicación iniciada!" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:4200" -ForegroundColor White
Write-Host "Backend: http://127.0.0.1:5000" -ForegroundColor White
Write-Host "Swagger: http://127.0.0.1:5000/swagger" -ForegroundColor White
#!/usr/bin/env powershell

Write-Host "=== Test CORS API Tareas ===" -ForegroundColor Green

# Test 1: Verificar que el backend responde
Write-Host "`n1. Verificando backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -Method GET -UseBasicParsing
    Write-Host "✅ Backend funcionando - Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend no responde: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Verificar headers CORS
Write-Host "`n2. Verificando headers CORS..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/register" -Method OPTIONS -UseBasicParsing
    $corsHeaders = $response.Headers
    
    if ($corsHeaders['Access-Control-Allow-Origin']) {
        Write-Host "✅ CORS Origin configurado: $($corsHeaders['Access-Control-Allow-Origin'])" -ForegroundColor Green
    } else {
        Write-Host "❌ CORS Origin no configurado" -ForegroundColor Red
    }
    
    if ($corsHeaders['Access-Control-Allow-Methods']) {
        Write-Host "✅ CORS Methods configurados: $($corsHeaders['Access-Control-Allow-Methods'])" -ForegroundColor Green
    } else {
        Write-Host "❌ CORS Methods no configurados" -ForegroundColor Red
    }
    
} catch {
    Write-Host "⚠️  Error verificando CORS: $($_.Exception.Message)" -ForegroundColor Orange
}

# Test 3: Test de registro
Write-Host "`n3. Test de registro..." -ForegroundColor Yellow
$registroData = @{
    usuario = "testcors_$(Get-Random)"
    email = "testcors@example.com"
    password = "123456"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $registroData `
        -UseBasicParsing
        
    Write-Host "✅ Registro exitoso - Status: $($response.StatusCode)" -ForegroundColor Green
    
    # Test 4: Test de login
    Write-Host "`n4. Test de login..." -ForegroundColor Yellow
    $loginData = @{
        usuario = ($registroData | ConvertFrom-Json).usuario
        password = "123456"
    } | ConvertTo-Json
    
    $loginResponse = Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginData `
        -UseBasicParsing
        
    Write-Host "✅ Login exitoso - Status: $($loginResponse.StatusCode)" -ForegroundColor Green
    
    $token = ($loginResponse.Content | ConvertFrom-Json).access_token
    Write-Host "🔑 Token obtenido: $($token.Substring(0,20))..." -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Error en prueba de API: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Frontend Angular ===" -ForegroundColor Green
Write-Host "🌐 Abre el navegador en: http://localhost:4200" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://127.0.0.1:5000/swagger" -ForegroundColor Cyan

Write-Host "`n✅ Tests CORS completados!" -ForegroundColor Green
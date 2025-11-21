# Test básico del backend
from app import create_app

# Crear la aplicación
app = create_app()

# Imprimir rutas disponibles
print("=== RUTAS DISPONIBLES ===")
with app.app_context():
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} {rule.rule}")

print("\n=== PROBANDO BACKEND ===")

# Crear un cliente de prueba
with app.test_client() as client:
    # Test 1: Endpoint raíz
    try:
        response = client.get('/')
        print(f"✅ GET / -> {response.status_code}: {response.get_json()}")
    except Exception as e:
        print(f"❌ Error en GET /: {e}")
    
    # Test 2: Registro
    try:
        response = client.post('/auth/register', 
                             json={'usuario': 'test', 'email': 'test@test.com', 'password': '123'})
        print(f"✅ POST /auth/register -> {response.status_code}: {response.get_json()}")
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        
    # Test 3: Login
    try:
        response = client.post('/auth/login', 
                             json={'usuario': 'test', 'password': '123'})
        print(f"✅ POST /auth/login -> {response.status_code}: {response.get_json()}")
    except Exception as e:
        print(f"❌ Error en login: {e}")

print("\n=== PRUEBAS COMPLETADAS ===")
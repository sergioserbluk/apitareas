  # punto de entrada
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource
from dotenv import load_dotenv

load_dotenv()
from extensions import db, jwt
from routes import api as tareas_api
from auth import api as auth_api

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "cambiar_esto")

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    
    # Configuración CORS ULTRA PERMISIVA para desarrollo
    CORS(app, 
         origins=["*"],  # Permitir todos los orígenes temporalmente 
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["*"],
         supports_credentials=False)  # Deshabilitar credentials temporalmente

    # Crear la API
    api = Api(
        app,
        title='API de Tareas',
        version='1.0',
        description='API REST de tareas con autenticación JWT',
        doc='/swagger',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        },
        security='Bearer'
    )

    # Registrar namespaces de la API
    api.add_namespace(tareas_api, path='/tareas')
    api.add_namespace(auth_api, path='/auth')

    # Crear namespace para endpoints base
    base_api = api.namespace('', description='Endpoints base')
    
    @base_api.route('/')
    class Root(Resource):
        @base_api.doc('root')
        def get(self):
            """Endpoint raíz que muestra información de la API"""
            return {"mensaje": "API de Tareas (Nivel 4) lista", "docs": "/swagger"}
    
    # Endpoint simple para verificar CORS
    @base_api.route('/test')
    class Test(Resource):
        def get(self):
            """Endpoint de prueba"""
            return {"status": "OK", "message": "Backend funcionando correctamente"}
        
        def post(self):
            """Endpoint de prueba POST"""
            return {"status": "OK", "message": "POST funcionando"}

    # Errores
    from utils import register_error_handlers
    register_error_handlers(app)

    return app

if __name__ == "__main__":

    # Crear la aplicación sólo cuando se ejecuta como script para evitar import cycles
    app = create_app()

    with app.app_context():

        from models import Tarea, Usuario

        db.create_all() # crea las tablas si no existen

    # Disable the auto-reloader here so the process stays attached during tests
    app.run(debug=True, host='127.0.0.1', port=5001)


  # punto de entrada
import os
import json
from flask import Flask, jsonify
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
    CORS(app)  # en prod: CORS(app, resources={r"/api/*": {"origins": "https://tu-dominio"}})

    # Crear la API
    api = Api(
        title='API de Tareas',
        version='1.0',
        description='API REST de tareas con autenticación JWT',
        doc='/swagger',
        prefix='/api/v1',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        },
        security='Bearer'
    )

    # Registrar la API con la app
    api.init_app(app)

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
            return {"mensaje": "API de Tareas (Nivel 4) lista", "docs": "/apidocs"}

    @base_api.route('/tareas')
    class PublicTasks(Resource):
        @base_api.doc('public_tasks')
        def get(self):
            """Endpoint público para pruebas (CORS / HTML). Devuelve el contenido de storage.json"""
            try:
                with app.open_resource("storage.json") as f:
                    data = json.load(f)
            except Exception:
                data = []
            return data, 200

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
    app.run(debug=True, use_reloader=False)


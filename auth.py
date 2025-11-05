 # login/registro y helpers JWT
from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import Usuario

api = Namespace('auth', description='Operaciones de autenticación')

# Modelos para la documentación
registro_model = api.model('Registro', {
    'usuario': fields.String(required=True, description='Nombre de usuario'),
    'email': fields.String(required=True, description='Correo electrónico'),
    'password': fields.String(required=True, description='Contraseña')
})

login_model = api.model('Login', {
    'usuario': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

@api.route('/register')
class Register(Resource):
    @api.expect(registro_model)
    @api.response(201, 'Usuario creado')
    @api.response(400, 'Datos inválidos')
    def post(self):
        """Registro de usuario"""
        data = request.get_json() or {}
        usuario = data.get("usuario", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not usuario or not email or not password:
            return {"error": "Faltan campos"}, 400

        if Usuario.query.filter((Usuario.usuario==usuario)|(Usuario.email==email)).first():
            return {"error": "Usuario o email ya existe"}, 400

        u = Usuario(
            usuario=usuario,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(u)
        db.session.commit()

        return {"mensaje": "Usuario creado", "id": u.id}, 201



@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login exitoso')
    @api.response(401, 'Credenciales inválidas')
    def post(self):
        """Login de usuario"""
        data = request.get_json() or {}
        usuario = data.get("usuario", "")
        password = data.get("password", "")

        u = Usuario.query.filter_by(usuario=usuario).first()
        if not u or not check_password_hash(u.password_hash, password):
            return {"error": "Credenciales inválidas"}, 401

        token = create_access_token(identity=str(u.id))
        return {"token": token}, 200

@api.route('/me')
class UserInfo(Resource):
    @jwt_required()
    @api.response(200, 'Datos del usuario')
    @api.response(401, 'No autorizado')
    def get(self):
        """Obtener datos del usuario autenticado"""
        uid = get_jwt_identity()
        u = Usuario.query.get(uid)
        return {"id": u.id, "usuario": u.usuario, "email": u.email}

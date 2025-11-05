 # endpoints CRUD
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Tarea

api = Namespace('tareas', description='Operaciones con tareas')

# Modelos para la documentación
tarea_model = api.model('Tarea', {
    'titulo': fields.String(required=True, description='Título de la tarea'),
    'hecha': fields.Boolean(required=False, description='Estado de la tarea')
})

@api.route('')
class TareasList(Resource):
    @api.doc('listar_tareas', security='Bearer')
    @jwt_required()
    def get(self):
        """Listar tareas del usuario autenticado"""
        uid = int(get_jwt_identity())
        tareas = Tarea.query.filter_by(usuario_id=uid).all()
        return [t.to_dict() for t in tareas], 200

    @api.doc('crear_tarea', security='Bearer')
    @api.expect(tarea_model)
    @jwt_required()
    def post(self):
        """Crear una nueva tarea"""
        data = request.get_json() or {}
        titulo = (data.get("titulo") or "").strip()
        hecha = bool(data.get("hecha", False))

        if not titulo:
            return {"error": "El título es requerido"}, 400

        uid = int(get_jwt_identity())
        t = Tarea(titulo=titulo, hecha=hecha, usuario_id=uid)
        db.session.add(t)
        db.session.commit()
        return t.to_dict(), 201

@api.route('/<int:tid>')
class TareaDetail(Resource):
    @api.doc('obtener_tarea', security='Bearer')
    @jwt_required()
    def get(self, tid):
        """Obtener una tarea específica"""
        uid = int(get_jwt_identity())
        t = Tarea.query.filter_by(id=tid, usuario_id=uid).first()
        if not t:
            return {"error": "No encontrada"}, 404
        return t.to_dict(), 200

    @api.doc('actualizar_tarea', security='Bearer')
    @api.expect(tarea_model)
    @jwt_required()
    def put(self, tid):
        """Actualizar una tarea existente"""
        uid = int(get_jwt_identity())
        t = Tarea.query.filter_by(id=tid, usuario_id=uid).first()
        if not t:
            return {"error": "No encontrada"}, 404

        data = request.get_json() or {}
        if "titulo" in data:
            nuevo = (data.get("titulo") or "").strip()
            if not nuevo:
                return {"error": "El título no puede ser vacío"}, 400
            t.titulo = nuevo

        if "hecha" in data:
            t.hecha = bool(data["hecha"])

        db.session.commit()
        return t.to_dict(), 200

    @api.doc('borrar_tarea', security='Bearer')
    @jwt_required()
    def delete(self, tid):
        """Eliminar una tarea"""
        uid = int(get_jwt_identity())
        t = Tarea.query.filter_by(id=tid, usuario_id=uid).first()
        if not t:
            return {"error": "No encontrada"}, 404
        db.session.delete(t)
        db.session.commit()
        return {"mensaje": f"Tarea {tid} eliminada"}, 200
# validaciones, helpers, errores
from flask import jsonify

def register_error_handlers(app):

    @app.errorhandler(400)

    def bad_request(e):

        return jsonify(error="Solicitud inválida"), 400

    @app.errorhandler(401)

    def unauthorized(e):

        return jsonify(error="No autorizado"), 401

    @app.errorhandler(404)

    def not_found(e):

        return jsonify(error="Recurso no encontrado"), 404

    @app.errorhandler(405)

    def method_not_allowed(e):

        return jsonify(error="Método no permitido"), 405

    @app.errorhandler(500)

    def internal_error(e):

        return jsonify(error="Error interno del servidor"), 500




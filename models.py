 # modelos SQLAlchemy
from datetime import datetime

from extensions import db

class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    usuario = db.Column(db.String(80), unique=True, nullable=False)

    email   = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    creado = db.Column(db.DateTime, default=datetime.utcnow)

    tareas = db.relationship("Tarea", backref="duenio", lazy=True)

class Tarea(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(100), nullable=False)

    hecha  = db.Column(db.Boolean, default=False)

    creado = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    def to_dict(self):

        return {

            "id": self.id,

            "titulo": self.titulo,

            "hecha": self.hecha,

            "creado": self.creado.isoformat(),

            "usuario_id": self.usuario_id

        }


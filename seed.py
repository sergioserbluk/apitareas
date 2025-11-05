from app import create_app
from extensions import db
from werkzeug.security import generate_password_hash

def seed():
    app = create_app()
    with app.app_context():
        from models import Usuario, Tarea

        db.create_all()

        if not Usuario.query.filter_by(usuario='demo').first():
            u = Usuario(usuario='demo', email='demo@example.com', password_hash=generate_password_hash('secret'))
            db.session.add(u)
            db.session.commit()

            t1 = Tarea(titulo='Tarea demo 1', hecha=False, usuario_id=u.id)
            t2 = Tarea(titulo='Tarea demo 2', hecha=True, usuario_id=u.id)
            db.session.add_all([t1, t2])
            db.session.commit()
            print('Seed: usuario demo creado con password "secret" y 2 tareas')
        else:
            print('Seed: usuario demo ya existe')

if __name__ == '__main__':
    seed()

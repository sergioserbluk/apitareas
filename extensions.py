from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Instancias compartidas de extensiones
db = SQLAlchemy()
jwt = JWTManager()

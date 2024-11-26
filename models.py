from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Configuración de la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Modelo User
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('admin', 'student', 'teacher'), nullable=False)
    identificacion = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    career = db.Column(db.String(120))
    semester = db.Column(db.String(120))

    # Relación con las tutorías inscritas
    tutorias_inscritas = db.relationship('Suscripcion', back_populates='user', cascade='all, delete-orphan')

    # Relación con las tutorías asignadas (para los docentes)
    tutorias_asignadas = db.relationship('Tutoria', back_populates='teacher')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# Modelo Tutoria
class Tutoria(db.Model):
    __tablename__ = 'tutoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tema = db.Column(db.String(200))
    compromiso = db.Column(db.String(200))
    horario = db.Column(db.DateTime)
    ubicacion = db.Column(db.String(100))
    docente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con los estudiantes a través de la tabla de suscripciones
    suscripciones = db.relationship('Suscripcion', back_populates='tutoria', cascade='all, delete-orphan')

    # Relación con el docente
    teacher = db.relationship('User', back_populates='tutorias_asignadas')

# Modelo Suscripcion
class Suscripcion(db.Model):
    __tablename__ = 'suscripciones'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tutoria_id = db.Column(db.Integer, db.ForeignKey('tutoria.id'), nullable=False)

    # Relaciones bidireccionales
    user = db.relationship('User', back_populates='tutorias_inscritas')
    tutoria = db.relationship('Tutoria', back_populates='suscripciones')

# Crear las tablas basadas en los modelos
def create_tables(app):
    with app.app_context():
        db.create_all()

# Crear las tablas basadas en los modelos
with app.app_context():
    db.create_all()
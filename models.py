from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):  # Asegúrate de heredar de UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('admin', 'student', 'teacher'), nullable=False)
    identificacion = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    career = db.Column(db.String(120))
    semester = db.Column(db.String(120))

    # Relación con las salas asignadas (si es docente)
    salas_asignadas = db.relationship('Sala', back_populates='docente', foreign_keys='Sala.docente_id')
    
    # Relación con las suscripciones
    suscripciones = db.relationship('Suscripcion', back_populates='user', cascade='all, delete-orphan')

    # Relación con las salas inscritas
    salas_inscritas = db.relationship('Sala', secondary='suscripciones', back_populates='estudiantes')


    # Sobreescribir el método is_active para que siempre devuelva True
    @property
    def is_active(self):
        return True

    # Método para establecer la contraseña de forma segura
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Método para verificar la contraseña
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)



class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_sala = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    horario = db.Column(db.String(100), nullable=True)
    ubicacion = db.Column(db.String(100), nullable=True)

    # Relación con el docente
    docente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    docente = db.relationship('User', back_populates='salas_asignadas')

    # Relación con los estudiantes
    estudiantes = db.relationship('User', secondary='suscripciones', back_populates='salas_inscritas')

    # Relación con las suscripciones
    suscripciones = db.relationship('Suscripcion', back_populates='sala')


class Suscripcion(db.Model):
    __tablename__ = 'suscripciones'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)

    # Relaciones
    user = db.relationship('User', back_populates='suscripciones')
    sala = db.relationship('Sala', back_populates='suscripciones')




from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Inicializa Flask-Bcrypt

# Define el modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('admin', 'student', 'teacher'), nullable=False)
    identificacion = db.Column(db.String(50), unique=True, nullable=False)

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

# Función para crear un usuario administrador
def create_admin_user():
    username = 'amd'
    password = '1234'  # Cambia por la contraseña deseada
    role = 'admin'
    identificacion = '8787'  # Un identificador único

    # Verificar si el usuario ya existe
    existing_user = User.query.filter((User.username == username) | (User.identificacion == identificacion)).first()

    if existing_user:
        print('No se puede crear el usuario: ya existe un usuario con el mismo username o identificacion.')
    else:
        # Encriptar la contraseña usando Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Crear el usuario
        admin_user = User(username=username, password=hashed_password, role=role, identificacion=identificacion)

        # Agregar y guardar en la base de datos
        db.session.add(admin_user)
        db.session.commit()
        print('Usuario administrador creado con éxito.')

# Llama a la función para crear el usuario
with app.app_context():
    create_admin_user()

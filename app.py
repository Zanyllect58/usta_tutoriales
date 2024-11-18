from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from models import User, db

app = Flask(__name__, template_folder='templates')  # Asegúrate de que 'templates' sea la carpeta correcta
app.config.from_object(Config)
db.init_app(app)  # Inicializa la base de datos con la app

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')

# Rutas relacionadas con el dashboard y la administración
@app.route('/dashboard_admin')
def dashboard():
    return render_template('admin/dashboard_admin.html')

@app.route('/dashboard_usuarios')
def dashboard_usuarios():
    return render_template('usuario/dashboard_usuarios.html')

# Rutas relacionadas con la gestión de usuarios
@app.route('/dashboard_admin_usuarios', methods=['GET'])
def users():
    users = User.query.all()
    return render_template('admin/dashboard_admin_usuarios.html', users=users)

@app.route('/registrar_usuarios')
def crear_usuario():
    return render_template('registrar.html')  # Ruta correcta si está directamente en templates

@app.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        career = request.form['career']
        semester = request.form['semester']

        existing_user = User.query.filter(
            ((User.username == username)) &
            (User.id != user_id)
        ).first()

        if existing_user:
            if existing_user.email == email:
                flash('El correo ya está en uso. Elige otro', 'danger')
            return redirect(url_for('editar_usuario'))
        
        user.username = username
        user.email = email
        user.role = role
        user.career = career
        user.semester = semester

        db.session.commit()
        return redirect(url_for('users'))

    return render_template('admin/dashboard_admin_usuarios_editar_usuarios.html', user = user)  # Ruta correcta en la carpeta admin

@app.route('/eliminar_usuario')
def eliminar_usuario():
    return render_template('admin/dashboard_admin_usuarios.html')  # Ruta correcta en la carpeta admin

# Rutas relacionadas con salas
@app.route('/crear_sala')
def crear_sala():
    return render_template('admin/dashboard_admin_crear_sala.html')

# Ruta para la página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Ejecutar la aplicación en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)

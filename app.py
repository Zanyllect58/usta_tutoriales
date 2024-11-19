from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from models import User, db,bcrypt, mysql


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

@app.route('/dashboard_docentes')
def dashboard_docentes():
    return render_template('docentes/dashboard_docentes.html')


# Rutas relacionadas con la gestión de usuarios
@app.route('/dashboard_admin_usuarios', methods=['GET'])
def users():
    user = User.query.all()  # Cambié 'user' a 'users'
    return render_template('admin/dashboard_admin_usuarios.html', user =user)  # Cambié 'user' a 'users'

@app.route('/registrar', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        # Recolectar datos del formulario
        username = request.form['nombre']    
        email = request.form['email'] 
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8') 
        role = 'student'  # Asignar rol de estudiante por defecto
        identificacion = request.form['confirm-number']  # Actualización aquí
        career = request.form['carrera']
        semester = request.form['semestre']

        # Crear nuevo usuario
        new_user = User(username=username, email=email, password=password, role=role,
                        identificacion=identificacion, career=career, semester=semester)

        # Guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()
        
        flash("Estudiante agregado correctamente.", "success")  # Mensaje de éxito
        return redirect(url_for('crear_usuario'))  # Redirigir para evitar reenvíos de formularios
    
    return render_template('registrar.html')



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

@app.route('/eliminar_usuario/<int:user_id>', methods=['POST', 'GET'])
def eliminar_usuario(user_id):
    # Buscar al usuario por su ID
    user = User.query.get(user_id)
    if not user:
        flash("El usuario no existe.", "danger")
        return redirect(url_for('users'))

    # Eliminar el usuario
    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for('users'))


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

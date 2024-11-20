from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from config import Config
from models import User, Suscripcion, Sala , db, bcrypt

# Inicialización de la aplicación Flask
app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db.init_app(app)

# Inicializar LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Función que carga el usuario por su id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =============================
# Rutas de Autenticación
# =============================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')

            # Redirigir según el rol del usuario
            if user.role == 'admin':
                return redirect(url_for('dashboard_admin'))
            elif user.role == 'teacher':
                return redirect(url_for('dashboard_docentes'))
            elif user.role == 'student':
                return redirect(url_for('dashboard_usuarios'))
        else:
            flash('Credenciales incorrectas. Intenta nuevamente.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('inicio'))

# =============================
# Rutas de Dashboard
# =============================

# Dashboard para Administradores
@app.route('/dashboard_admin')
@login_required
def dashboard_admin():
    if current_user.role != 'admin':  # Verificar si es admin
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('inicio'))
    return render_template('admin/dashboard_admin.html')

# Dashboard para Estudiantes
@app.route('/dashboard_usuarios')
@login_required
def dashboard_usuarios():
    user = current_user
    salas = Sala.query.all()
    suscripciones = user.suscripciones
    suscripciones_ids = [sala.id for sala in suscripciones]
    return render_template('usuario/dashboard_usuarios.html', salas=salas, suscripciones_ids=suscripciones_ids)

# Dashboard para Docentes
@app.route('/dashboard_docentes')
@login_required
def dashboard_docentes():
    if current_user.role != 'teacher':  # Verificar si es docente
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('inicio'))
    
    # Obtener las salas asignadas al docente
    salas_docente = Sala.query.filter_by(docente_id=current_user.id).all()
    return render_template('docentes/dashboard_docentes.html', salas=salas_docente)

# =============================
# Rutas de Gestión de Usuarios (Admin)
# =============================

# Listar todos los usuarios (solo admin)
@app.route('/dashboard_admin_usuarios', methods=['GET'])
@login_required
def users():
    if current_user.role != 'admin':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('inicio'))

    user = User.query.all()
    return render_template('admin/dashboard_admin_usuarios.html', user=user)

# Crear Usuario (solo admin)
@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if current_user.role != 'admin':  # Asegurar que solo el admin puede crear usuarios
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))
    
    if request.method == 'POST':
        user_data = {
            'username': request.form['nombre'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
            'role': 'student',
            'identificacion': request.form['confirm-number'],
            'career': request.form['carrera'],
            'semester': request.form['semestre']
        }

        if User.query.filter_by(email=user_data['email']).first():
            flash('El correo ya está en uso. Elige otro.', 'danger')
            return redirect(url_for('crear_usuario'))

        if User.query.filter_by(identificacion=user_data['identificacion']).first():
            flash('La identificación ya está en uso. Elige otra.', 'danger')
            return redirect(url_for('crear_usuario'))

        try:
            new_user = User(**user_data)
            db.session.add(new_user)
            db.session.commit()
            flash("Estudiante agregado correctamente.", "success")
            return redirect(url_for('crear_usuario'))
        except Exception as e:
            db.session.rollback()  # Si ocurre un error, revertimos la transacción
            flash(f"Error al agregar el estudiante: {str(e)}", "danger")
            return redirect(url_for('crear_usuario'))

    return render_template('registrar.html')

# Editar Usuario (solo admin)
@app.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(user_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))

    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        user.career = request.form['career']
        user.semester = request.form['semester']

        if User.query.filter((User.email == user.email) & (User.id != user_id)).first():
            flash('El correo ya está en uso. Elige otro.', 'danger')
            return redirect(url_for('editar_usuario', user_id=user_id))

        try:
            db.session.commit()
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for('users'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el usuario: {str(e)}", "danger")
            return redirect(url_for('editar_usuario', user_id=user_id))

    return render_template('admin/dashboard_admin_usuarios_editar_usuarios.html', user=user)

# Eliminar Usuario (solo admin)
@app.route('/eliminar_usuario/<int:user_id>', methods=['POST', 'GET'])
@login_required
def eliminar_usuario(user_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))

    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash("Usuario eliminado correctamente.", "success")
        else:
            flash("El usuario no existe.", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el usuario: {str(e)}", "danger")
    
    return redirect(url_for('users'))

# =============================
# Rutas de Gestión de Salas
# =============================

# Crear Sala (solo admin)
@app.route('/crear_sala', methods=['GET', 'POST'])
@login_required
def crear_sala():
    if current_user.role != 'admin':
        return jsonify({'error': 'No tienes permisos para crear una sala.'}), 403

    docentes = User.query.filter_by(role='teacher').all()

    if request.method == 'POST':
        nombre_sala = request.form.get('nombre-sala')
        descripcion = request.form.get('descripcion')
        horario = request.form.get('horario')
        ubicacion = request.form.get('ubicacion')
        docente_id = request.form.get('docente')

        if not nombre_sala:
            return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes, mensaje="El nombre de la sala es obligatorio.", mensaje_color="red")
        if not descripcion:
            return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes, mensaje="La descripción es obligatoria.", mensaje_color="red")
        if not horario:
            return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes, mensaje="El horario es obligatorio.", mensaje_color="red")
        if not ubicacion:
            return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes, mensaje="La ubicación es obligatoria.", mensaje_color="red")
        if not docente_id:
            return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes, mensaje="Debes seleccionar un docente para la sala.", mensaje_color="red")

        docente = User.query.get(docente_id)
        if not docente or docente.role != 'teacher':
            return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes, mensaje="El docente seleccionado no es válido.", mensaje_color="red")

        try:
            nueva_sala = Sala(nombre=nombre_sala, descripcion=descripcion, horario=horario, ubicacion=ubicacion, docente_id=docente_id)
            db.session.add(nueva_sala)
            db.session.commit()
            flash("Sala creada correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear la sala: {str(e)}", "danger")
            return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes, mensaje="Error al crear la sala.", mensaje_color="red")

    return render_template('admin/dashboard_admin_crear_sala.html', docentes=docentes)



# =============================
# Rutas de Gestión de Suscripciones
# =============================

# Suscribirse a una Sala
@app.route('/suscribirse_sala/<int:sala_id>', methods=['POST'])
@login_required
def suscribirse_sala(sala_id):
    sala = Sala.query.get(sala_id)
    if not sala:
        return jsonify({"status": "error", "message": "Sala no encontrada"}), 404

    if any(s.id == sala_id for s in current_user.suscripciones):
        return jsonify({"status": "error", "message": "Ya estás suscrito a esta sala"}), 400

    nueva_suscripcion = Suscripcion(user_id=current_user.id, sala_id=sala.id)
    db.session.add(nueva_suscripcion)
    db.session.commit()
    return jsonify({"status": "success", "action": "unirse"})

# Eliminar Suscripción de una Sala
@app.route('/eliminar_suscripcion/<int:sala_id>', methods=['POST'])
@login_required
def eliminar_suscripcion(sala_id):
    sala = Sala.query.get(sala_id)
    if not sala:
        return jsonify({"status": "error", "message": "Sala no encontrada"}), 404

    suscripcion = Suscripcion.query.filter_by(user_id=current_user.id, sala_id=sala_id).first()
    if not suscripcion:
        return jsonify({"status": "error", "message": "No estás suscrito a esta sala"}), 400

    db.session.delete(suscripcion)
    db.session.commit()
    return jsonify({"status": "success", "action": "eliminar"})



# =============================
# Rutas de Gestión de Docentes
# =============================


@app.route('/ver_estudiantes/<int:sala_id>')
def ver_estudiantes(sala_id):
    # Lógica de la vista
    return render_template('ver_estudiantes.html', sala_id=sala_id)

# =============================
# Rutas de Gestión de Principales
# =============================


@app.route('/')
def inicio ():
    # Lógica de la vista
    return render_template('index.html')



# =============================
# Ejecución de la Aplicación
# =============================

if __name__ == '__main__':
    app.run(debug=True)
    

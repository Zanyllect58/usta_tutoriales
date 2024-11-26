from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify 
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from config import Config
from models import User, Suscripcion, Tutoria, db, bcrypt
from datetime import datetime


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
    return db.session.get(User, int(user_id))  # Uso de Session.get() en lugar de Query.get()

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

            # Guardar el nombre de usuario en la sesión
            session['user_name'] = user.username  # Aquí se guarda el nombre del usuario en la sesión

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
# Rutas de Gestión de Tutorias
# =============================

@app.route('/crear_tutoria', methods=['GET', 'POST'])
@login_required
def crear_tutoria():
    if current_user.role != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))

    docentes = User.query.filter_by(role='teacher').all()

    if request.method == 'POST':
        nombre = request.form.get('nombre-tutoria')
        docente_id = request.form.get('docente')
        compromiso = ""

        if not all([nombre, docente_id]):
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('admin/dashboard_admin_crear_tutoria.html', docentes=docentes)

        try:
            nueva_tutoria = Tutoria(
                nombre=nombre,
                docente_id=docente_id,
                compromiso = compromiso
            )
            db.session.add(nueva_tutoria)
            db.session.commit()
            flash('Tutoría creada correctamente.', 'success')
            return redirect(url_for('listar_tutorias'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la tutoría: {str(e)}', 'danger')

    return render_template('admin/dashboard_admin_crear_tutoria.html', docentes=docentes)

# Listar todas las tutorías (solo admin)
@app.route('/dashboard_admin_tutorias', methods=['GET'])
@login_required
def listar_tutorias():
    if current_user.role != 'admin':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('inicio'))

    tutorias = Tutoria.query.all()
    return render_template('admin/dashboard_admin_tutorias.html', tutorias=tutorias)

# Editar una tutoría (solo admin)
@app.route('/editar_tutoria/<int:tutoria_id>', methods=['GET', 'POST'])
@login_required
def editar_tutoria(tutoria_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))

    tutoria = Tutoria.query.get_or_404(tutoria_id)
    docentes = User.query.filter_by(role='teacher').all()

    if request.method == 'POST':
        tutoria.nombre = request.form['nombre-tutoria']
        tutoria.tema = request.form['tema']
        tutoria.horario = request.form['horario']
        tutoria.ubicacion = request.form['ubicacion']
        tutoria.docente_id = request.form['docente']

        try:
            db.session.commit()
            flash('Tutoría actualizada correctamente.', 'success')
            return redirect(url_for('listar_tutorias'))
        except Exception as e:
            db.session .rollback()
            flash(f'Error al actualizar la tutoría: {str(e)}', 'danger')

    return render_template('admin/dashboard_admin_editar_tutoria.html', tutoria=tutoria, docentes=docentes)

# Eliminar una tutoría (solo admin)
@app.route('/eliminar_tutoria/<int:tutoria_id>', methods=['POST'])
@login_required
def eliminar_tutoria(tutoria_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))

    tutoria = Tutoria.query.get_or_404(tutoria_id)

    try:
        db.session.delete(tutoria)
        db.session.commit()
        flash('Tutoría eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la tutoría: {str(e)}', 'danger')

    return redirect(url_for('listar_tutorias'))

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

        if User.query.filter((User .email == user.email) & (User .id != user_id)).first():
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


# Agregar Usuario (solo admin)

@app.route('/agregar_usuario', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    if current_user.role != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))
    
    if request.method == 'POST':
        user_data = {
            'username': request.form['nombre'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
            'role': request.form['role'], 
            'identificacion': request.form['confirm-number'],
            'career': request.form['carrera'],
            'semester': request.form['semestre']
        }

        if User.query.filter_by(email=user_data['email']).first():
            flash('El correo ya está en uso. Elige otro.', 'danger')
            return render_template('admin/dashboard_admin_usuarios_agregar_usuarios.html')  

        if User.query.filter_by(identificacion=user_data['identificacion']).first():
            flash('La identificación ya está en uso. Elige otra.', 'danger')
            return render_template('admin/dashboard_admin_usuarios_agregar_usuarios.html')  

        try:
            # Crear el nuevo usuario
            new_user = User(**user_data)
            db.session.add(new_user)
            db.session.commit()

            flash("Usuario agregado correctamente.", "success")
            return redirect(url_for('users'))  # Redirigir al inicio o página correspondiente después del registro
        except Exception as e:
            db.session.rollback()
            flash(f"Error al agregar el estudiante: {str(e)}", "danger")
            return render_template('admin/dashboard_admin_usuarios_agregar_usuarios.html')  # Redirigir a la misma página en caso de error

    return render_template('admin/dashboard_admin_usuarios_agregar_usuarios.html')



# =============================
# Rutas de Gestión de Tutorías
# =============================

# Dashboard para Administradores
@app.route('/dashboard_admin')
@login_required
def dashboard_admin():
    if current_user.role != 'admin':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('inicio'))

    total_usuarios = User.query.count()
    inicio_mes = datetime.now().replace(day=1)
    total_tutoria_mes = Tutoria.query.filter(Tutoria.fecha >= inicio_mes).count()

    usuarios = User.query.all()
    tutorias = Tutoria.query.all()

    return render_template(
        'admin/dashboard_admin.html',
        total_usuarios=total_usuarios,
        total_tutorias_mes=total_tutoria_mes,
        usuarios=usuarios,
        tutorias=tutorias
    )

# Dashboard para Estudiantes
@app.route('/dashboard_usuarios')
@login_required
def dashboard_usuarios():
    user = current_user
    tutorias = Tutoria.query.all()
    suscripciones = user.suscripciones
    suscripciones_ids = [tutoria.id for tutoria in suscripciones]

    # Obtener historial de sesiones (tutorias a las que está suscrito)
    historial = []
    for suscripcion in suscripciones:
        historial.append(suscripcion.tutoria)  # Accedemos a la tutoria relacionada con la suscripción

    return render_template('usuario/dashboard_usuarios.html', tutorias=tutorias, suscripciones_ids=suscripciones_ids, historial=historial)

# =============================
# Rutas de Gestión de Suscripciones
# =============================

@app.route('/suscribirse_tutoria/<int:tutoria_id>', methods=['POST'])
@login_required
def suscribirse_tutoria(tutoria_id):
    tutoria = Tutoria.query.get(tutoria_id)
    if not tutoria:
        return jsonify({"status": "error", "message": "tutoria no encontrada"}), 404

    # Verificar si ya está suscrito
    if any(t.id == tutoria_id for t in current_user.tutorias_inscritas):
        return jsonify({"status": "error", "message": "Ya estás suscrito a esta tutoria"}), 400

    # Crear nueva suscripción
    nueva_suscripcion = Suscripcion(user_id=current_user.id, tutoria_id=tutoria.id)
    db.session.add(nueva_suscripcion)
    db.session.commit()
    return jsonify({"status": "success", "action": "unirse"})

@app.route('/eliminar_suscripcion/<int:tutoria_id>', methods=['POST'])
@login_required
def eliminar_suscripcion(tutoria_id):
    tutoria = Tutoria.query.get(tutoria_id)
    if not tutoria:
        return jsonify({"status": "error", "message": "tutoria no encontrada"}), 404

    # Buscar suscripción
    suscripcion = Suscripcion.query.filter_by(user_id=current_user.id, tutoria_id=tutoria_id).first()
    if not suscripcion:
        return jsonify({"status": "error", "message": "No estás suscrito a esta tutoria"}), 400

    db.session.delete(suscripcion)
    db.session.commit()
    return jsonify({"status": "success", "action": "eliminar"})


# =============================
# Rutas de Gestión de Estudiantes
# =============================


# Dashboard para Docentes
@app.route('/dashboard_docentes')
@login_required
def dashboard_docentes():
    if current_user.role != 'teacher':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('inicio'))

    # Aquí puedes agregar cualquier lógica para que los docentes vean sus tutorias o tutorías asignadas
    tutorias = Tutoria.query.filter_by(docente_id=current_user.id).all()  # Obtener las tutorías asignadas al docente
    return render_template('docentes/dashboard_docentes.html', tutorias=tutorias)

# Editar una tutoría (solo docente)
@app.route('/editar_tutoria_docente/<int:tutoria_id>', methods=['GET', 'POST'])
@login_required
def editar_tutoria_docente(tutoria_id):
    if current_user.role != 'teacher':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))

    tutoria = Tutoria.query.get_or_404(tutoria_id)

    if request.method == 'POST':
        tutoria.tema = request.form['tema']
        tutoria.horario = request.form['horario']
        tutoria.ubicacion = request.form['ubicacion']

        try:
            db.session.commit()
            flash('Tutoría actualizada correctamente.', 'success')
            return redirect(url_for('dashboard_docentes'))
        except Exception as e:
            db.session .rollback()
            flash(f'Error al actualizar la tutoría: {str(e)}', 'danger')

    return render_template('docentes/dashboard_docentes_editar_tutoria.html', tutoria=tutoria)


@app.route('/ver_estudiantes/<int:tutoria_id>')
def ver_estudiantes(tutoria_id):
    tutoria = Tutoria.query.get(tutoria_id)
    return render_template('docentes/ver_estudiantes.html', tutoria=tutoria)

@app.route('/finalizar_tutoria/<int:tutoria_id>', methods=['GET', 'POST'])
def finalizar_tutoria(tutoria_id):
    if current_user.role != 'teacher':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('inicio'))

    tutoria = Tutoria.query.get_or_404(tutoria_id)

    if request.method == 'POST':
        tutoria.estado = False
        tutoria.compromiso = request.form['compromiso']

        try:
            db.session.commit()
            flash('Tutoría actualizada correctamente.', 'success')
            return redirect(url_for('dashboard_docentes'))
        except Exception as e:
            db.session .rollback()
            flash(f'Error al actualizar la tutoría: {str(e)}', 'danger')

    return render_template('docentes/dashboard_docentes_finalizar_tutoria.html', tutoria=tutoria)


# =============================
# Rutas de Gestión de Principales
# =============================

@app.route('/')
def inicio():
    return render_template('index.html')

# =============================
# Ejecución de la Aplicación
# =============================

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')  # Asegúrate de que 'templates' sea la carpeta correcta

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
@app.route('/dashboard_admin_usuarios')
def users():
    return render_template('admin/dashboard_admin_usuarios.html')

@app.route('/registrar_usuarios')
def crear_usuario():
    return render_template('registrar.html')  # Ruta correcta si está directamente en templates

@app.route('/editar_usuario')
def editar_usuario():
    return render_template('admin/dashboard_admin_usuarios_editar_usuarios.html')  # Ruta correcta en la carpeta admin

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

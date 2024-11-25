# Sistema de Gestión 


Este proyecto implementa un sistema de gestión  utilizando **Flask** y **SQLAlchemy**. El sistema permite manejar usuarios con diferentes roles (administradores, docentes y estudiantes), salas de tutoría, y suscripciones entre usuarios y salas.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes elementos:

- Python 3.7 o superior
- MySQL o MariaDB
- **Librerías necesarias**:
  - Flask==2.3.2
  - Flask-SQLAlchemy==3.0.2
  - Flask-Login==0.6.2
  - Flask-WTF==1.0.1
  - Flask-Migrate==3.1.0

## Estructura del Proyecto

```bash

├── app.py                 # Punto de entrada de la aplicación
├── config.py              # Configuración de la aplicación (por ejemplo, base de datos, claves secretas)
├── models.py              # Modelos de base de datos con SQLAlchemy
├── templates/             # Plantillas HTML para renderizar las vistas
│   ├── index.html         # Página de inicio principal
│   ├── login.html         # Página de inicio de sesión
│   ├── registrar.html     # Formulario de registro de usuarios
│   ├── admin/             # Paneles de administración
│   │   ├── dashboard_admin.html                  # Dashboard principal para admin
│   │   ├── dashboard_admin_tutorias.html         # Gestión de tutorías
│   │   ├── dashboard_admin_crear_sala.html       # Formulario para crear salas
│   │   ├── dashboard_admin_editar_sala.html      # Formulario para editar salas
│   │   ├── dashboard_admin_usuarios.html         # Gestión de usuarios
│   │   ├── dashboard_admin_usuarios_agregar_usuarios.html  # Formulario para agregar usuarios
│   │   └── dashboard_admin_usuarios_editar_usuarios.html   # Formulario para editar usuarios
│   ├── usuario/           # Paneles para estudiantes
│   │   ├── dashboard_usuarios.html               # Dashboard para estudiantes
│   └── docentes/          # Paneles para docentes
│       ├── dashboard_docentes.html               # Dashboard para docentes
│       └── ver_estudiantes.html                  # Vista para listar estudiantes inscritos en una sala
├── static/                # Archivos estáticos como estilos CSS, imágenes y scripts JS
│   ├── css/               # Archivos CSS para estilos personalizados
│   └── img/               # Imágenes utilizadas en el sitio

```
# **Estructura de Endpoints de la Aplicación Flask**


Este documento describe los endpoints de la aplicación, organizados por su importancia y funcionalidad. Los endpoints se dividen en varias categorías según su propósito.

## 1. Rutas de Autenticación (Prioridad Alta)

Estas rutas son esenciales para la gestión de la sesión de los usuarios.

- **`/login`**: Iniciar sesión  
  `Método`: `GET, POST`  
  Permite a los usuarios iniciar sesión en el sistema.

- **`/logout`**: Cerrar sesión  
  `Método`: `GET`  
  Permite cerrar la sesión actual del usuario autenticado.

- **`/registrar`**: Crear nuevo usuario  
  `Método`: `GET, POST`  
  Permite crear nuevos usuarios en el sistema.

## 2. Rutas de Gestión de Salas (Para Administradores )

Estas rutas permiten la creación, edición, eliminación y visualización de salas de tutoría.

- **`/crear_sala`**: Crear nueva sala  
  `Método`: `GET, POST`  
  Permite a los administradores y docentes crear nuevas salas de tutoría.

- **`/dashboard_admin_tutorias`**: Listar tutorías  
  `Método`: `GET`  
  Muestra una lista de todas las tutorías disponibles en el sistema.

- **`/editar_sala/<int:sala_id>`**: Editar una sala  
  `Método`: `GET, POST`  
  Permite a los administradores y docentes editar los detalles de una sala de tutoría existente.

- **`/eliminar_sala/<int:sala_id>`**: Eliminar una sala  
  `Método`: `POST`  
  Permite eliminar una sala de tutoría existente.

## 3. Rutas de Gestión de Usuarios (Para Administradores)

Estas rutas permiten gestionar los usuarios del sistema, incluyendo la creación, edición, eliminación y listado de usuarios.

- **`/dashboard_admin_usuarios`**: Listar usuarios  
  `Método`: `GET`  
  Muestra una lista de todos los usuarios registrados en el sistema.

- **`/editar_usuario/<int:user_id>`**: Editar usuario  
  `Método`: `GET, POST`  
  Permite editar la información de un usuario existente.

- **`/eliminar_usuario/<int:user_id>`**: Eliminar usuario  
  `Método`: `POST, GET`  
  Permite eliminar un usuario del sistema.

- **`/agregar_usuario`**: Agregar usuario  
  `Método`: `GET, POST`  
  Permite agregar usuarios al sistema de forma manual.

## 4. Rutas de Gestión de Suscripciones (Para Estudiantes)

Permiten a los usuarios suscribirse y eliminar suscripciones de las salas.

- **`/suscribirse_sala/<int:sala_id>`**: Suscribirse a una sala  
  `Método`: `POST`  
  Permite a los usuarios suscribirse a una sala de tutoría.

- **`/eliminar_suscripcion/<int:sala_id>`**: Eliminar suscripción  
  `Método`: `POST`  
  Permite a los usuarios eliminar su suscripción a una sala de tutoría.

## 5. Rutas de Gestión de Tutorías (Vista de Estudiantes y Docentes)

Rutas para que los estudiantes y docentes gestionen o vean las tutorías a las que están inscritos.

- **`/dashboard_usuarios`**: Dashboard para estudiantes  
  `Método`: `GET`  
  Muestra el dashboard de las tutorías a las que el estudiante está suscrito.

- **`/dashboard_docentes`**: Dashboard para docentes  
  `Método`: `GET`  
  Muestra el dashboard de las tutorías que el docente está gestionando.

- **`/ver_estudiantes/<int:sala_id>`**: Ver estudiantes en una sala  
  `Método`: `GET`  
  Permite a los docentes ver la lista de estudiantes suscritos a una sala de tutoría.

## 6. Rutas Principales (No Requieren Autenticación)

Rutas generales de la aplicación que no requieren que el usuario esté autenticado.

- **`/`**: Página de inicio  
  `Método`: `GET`  
  Página principal de la aplicación.


## Instalación

1. Clona este repositorio: git clone https://github.com/Zanyllect58/usta_tutoriales.git

2. cd usta_tutoriales

3. python -m venv venv
   
4. venv\Scripts\activate

5. pip install -r requirements.txt
   
6. pip show mysql-connector-python
  
7. python user_admin.py
   
8. python models.py
   
9.  python app.py



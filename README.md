# Proyecto Final Compiladores - Aplicación Web CRUD

Esta es una aplicación web desarrollada en Python utilizando Flask y SQLAlchemy. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre una entidad principal (Productos) y cuenta con un sistema básico de autenticación de usuarios.

## Características

*   Framework Backend: Flask
*   ORM: SQLAlchemy
*   Base de Datos: SQLite (por defecto, configurable para PostgreSQL)
*   Frontend: HTML, CSS, Bootstrap
*   Autenticación de usuarios (Registro, Login, Logout)
*   Operaciones CRUD completas para la entidad "Productos".
*   Validaciones en frontend y backend.
*   Mensajes de retroalimentación al usuario.
*   Protección contra inyección SQL mediante el uso de SQLAlchemy.
*   Rutas protegidas que requieren autenticación.

## Requisitos

*   Python 3.7+
*   pip (manejador de paquetes de Python)
*   Git (opcional, para clonar el repositorio)

## Configuración del Entorno y Ejecución

1.  **Clonar el repositorio (opcional):**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO_DEL_PROYECTO>
    ```

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    Activar el entorno virtual:
    *   En Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   En macOS y Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno (opcional pero recomendado para producción):**
    Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```
    SECRET_KEY='tu_clave_secreta_personalizada'
    # Para PostgreSQL, usa algo como:
    # DATABASE_URL='postgresql://usuario:contraseña@host:puerto/nombre_db'
    # Para SQLite (por defecto si DATABASE_URL no está definida):
    # DATABASE_URL='sqlite:///site.db'
    ```
    La aplicación usará valores por defecto si estas variables no están definidas, pero `SECRET_KEY` debería ser única y secreta en producción.

5.  **Inicializar la base de datos:**
    La aplicación está configurada para crear las tablas de la base de datos automáticamente la primera vez que se ejecuta si no existen.

6.  **Ejecutar la aplicación:**
    ```bash
    flask run
    ```
    O también:
    ```bash
    python app.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000/` por defecto.

    Para ejecutar con Gunicorn (simulando un entorno de producción):
    ```bash
    gunicorn "app:create_app()"
    ```
    Esto asumirá que `app.py` contiene la factory `create_app()`. Gunicorn por defecto se enlaza a `127.0.0.1:8000`.

## Estructura del Proyecto

```
.
├── app.py            # Archivo principal de la aplicación, inicialización de Flask y extensiones.
├── config.py         # Configuración de la aplicación (BD, Clave Secreta).
├── models.py         # Modelos de datos SQLAlchemy (User, Product).
├── routes.py         # Lógica de las rutas y vistas de la aplicación.
├── requirements.txt  # Dependencias del proyecto.
├── static/           # Archivos estáticos (CSS, JavaScript, imágenes).
│   └── css/
│       └── style.css # Hoja de estilos personalizada.
├── templates/        # Plantillas HTML (Jinja2).
│   ├── base.html         # Plantilla base.
│   ├── login.html        # Formulario de login.
│   ├── register.html     # Formulario de registro.
│   ├── index.html        # Vista principal (lista de productos).
│   ├── create.html       # Formulario para crear productos.
│   ├── edit.html         # Formulario para editar productos.
│   └── _flashes.html     # Para mostrar mensajes flash.
├── README.md         # Este archivo.
└── instance/         # Carpeta donde se guardará site.db (SQLite) por defecto.
```

## Criterios de Evaluación (Materia Compiladores)

Este proyecto busca cumplir con los siguientes criterios:

1.  **Funcionalidad (80 pts):**
    *   Conexión exitosa a base de datos (SQLite por defecto).
    *   CRUD completo sobre la entidad "Productos".
    *   Coincidencia de datos entre UI y BD.
2.  **Interfaz de Usuario (8 pts):**
    *   Uso de HTML, CSS, Bootstrap para interfaz intuitiva.
    *   Validación de entradas (frontend y backend).
    *   Mensajes de retroalimentación.
3.  **Manejo de errores y seguridad en la conexión (2 pts):**
    *   Manejo de errores y excepciones.
    *   Uso de SQLAlchemy para prevenir inyección SQL.
4.  **Operaciones SQL (2 pts):**
    *   Operaciones CRUD seguras y eficientes.
    *   Transacciones implícitas por SQLAlchemy para operaciones individuales.
5.  **Documentación y presentación (2 pts):**
    *   Este `README.md` con la descripción, requisitos e instrucciones.
6.  **Escalabilidad y rendimiento (2 pts):**
    *   Código modularizado (separación en `app.py`, `routes.py`, `models.py`, `config.py`).
    *   Preparado para añadir nuevas entidades.
7.  **Calidad del código (2 pts):**
    *   Código legible, bien estructurado, comentarios relevantes.
    *   Nombres descriptivos.
8.  **Seguridad (2 pts):**
    *   Autenticación básica (login, register, logout).
    *   Protección de rutas sensibles.

## Despliegue (Ejemplos)

*   **Heroku:**
    1.  Asegúrate de tener `gunicorn` en `requirements.txt`.
    2.  Crea un `Procfile` en la raíz del proyecto:
        ```
        web: gunicorn "app:create_app()"
        ```
    3.  Configura la variable de entorno `DATABASE_URL` en Heroku (ej. Heroku Postgres).
    4.  Sigue las instrucciones de Heroku para desplegar una aplicación Python.

*   **Render:**
    1.  Asegúrate de tener `gunicorn` en `requirements.txt`.
    2.  En Render, crea un nuevo "Web Service".
    3.  Conecta tu repositorio Git.
    4.  Configura el "Build Command" (ej. `pip install -r requirements.txt`).
    5.  Configura el "Start Command" (ej. `gunicorn "app:create_app()"`).
    6.  Añade las variables de entorno necesarias (`SECRET_KEY`, `DATABASE_URL`).

---
Desarrollado como proyecto final para la materia de Compiladores.
```

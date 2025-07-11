import os
from flask import Flask
from flask_login import LoginManager
from models import db, User  # Importa User para el user_loader
from config import Config
# Importa las rutas después de crear la app y db para evitar importaciones circulares
# from routes import main_routes # Esto se hará al final de este archivo


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Nombre de la función de vista para login
    login_manager.login_message_category = 'info' # Categoría para mensajes flash

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importar y registrar Blueprints (rutas)
    # Es importante importar aquí para evitar importaciones circulares
    # y asegurar que 'app' y 'db' estén disponibles para las rutas.
    from routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        # Crear tablas de la base de datos si no existen
        # Esto es adecuado para desarrollo. Para producción,
        # se suelen usar migraciones (ej. Flask-Migrate).
        if not os.path.exists(os.path.join(app.instance_path, Config.SQLALCHEMY_DATABASE_URI.split('///')[-1])) or app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
            # Para SQLite, verificamos la existencia del archivo.
            # Para otras DBs, podríamos necesitar una estrategia diferente o asumir que create_all() es seguro.
            # O simplemente llamar a db.create_all() directamente si se manejan migraciones externamente.
            try:
                db.create_all()
                print("Base de datos y tablas creadas (si no existían).")
            except Exception as e:
                print(f"Error al crear las tablas de la base de datos: {e}")
        else:
            print("La base de datos ya existe, no se intentó crear tablas.")


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) # debug=True es útil para desarrollo, desactivar en producción.

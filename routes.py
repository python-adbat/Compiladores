from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product

# Usar un Blueprint para organizar las rutas
bp = Blueprint('main', __name__)

# --- Rutas de Autenticación ---

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones básicas
        if not username or len(username) < 4:
            flash('El nombre de usuario debe tener al menos 4 caracteres.', 'danger')
            return redirect(url_for('main.register'))
        if not password or len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return redirect(url_for('main.register'))
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('main.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Ese nombre de usuario ya existe. Por favor, elige otro.', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'danger')
            return redirect(url_for('main.register'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Por favor, ingresa usuario y contraseña.', 'danger')
            return redirect(url_for('main.login'))

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.login'))

# --- Rutas CRUD para Productos ---

@bp.route('/')
@bp.route('/products')
@login_required
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price_str = request.form.get('price')

        # Validaciones básicas
        if not name or len(name) < 3:
            flash('El nombre del producto debe tener al menos 3 caracteres.', 'danger')
            return render_template('create.html', name=name, description=description, price=price_str)

        if not price_str:
            flash('El precio es obligatorio.', 'danger')
            return render_template('create.html', name=name, description=description, price=price_str)

        try:
            price = float(price_str)
            if price < 0:
                flash('El precio no puede ser negativo.', 'danger')
                return render_template('create.html', name=name, description=description, price=price_str)
        except ValueError:
            flash('El precio debe ser un número válido.', 'danger')
            return render_template('create.html', name=name, description=description, price=price_str)

        new_product = Product(name=name, description=description, price=price)
        try:
            db.session.add(new_product)
            db.session.commit()
            flash('Producto creado exitosamente.', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el producto: {str(e)}', 'danger')
            # Pasar los datos de vuelta al formulario para no perderlos
            return render_template('create.html', name=name, description=description, price=price_str)

    return render_template('create.html')

@bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price_str = request.form.get('price')

        # Validaciones básicas
        if not name or len(name) < 3:
            flash('El nombre del producto debe tener al menos 3 caracteres.', 'danger')
            # Es importante pasar el objeto producto a la plantilla en caso de error
            return render_template('edit.html', product=product, name=name, description=description, price=price_str)

        if not price_str:
            flash('El precio es obligatorio.', 'danger')
            return render_template('edit.html', product=product, name=name, description=description, price=price_str)

        try:
            price = float(price_str)
            if price < 0:
                flash('El precio no puede ser negativo.', 'danger')
                return render_template('edit.html', product=product, name=name, description=description, price=price_str)
        except ValueError:
            flash('El precio debe ser un número válido.', 'danger')
            return render_template('edit.html', product=product, name=name, description=description, price=price_str)

        product.name = name
        product.description = description
        product.price = price
        try:
            db.session.commit()
            flash('Producto actualizado exitosamente.', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el producto: {str(e)}', 'danger')
            # Pasar el objeto producto modificado (pero no guardado) y los datos del formulario
            # para que el usuario pueda corregir
            product.name = name # Mantener los cambios no guardados en el objeto para el form
            product.description = description
            product.price = price_str # Usar el string original para el input
            return render_template('edit.html', product=product)

    # Para GET, pasar el producto existente al formulario
    return render_template('edit.html', product=product)

@bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Producto eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el producto: {str(e)}', 'danger')
    return redirect(url_for('main.index'))

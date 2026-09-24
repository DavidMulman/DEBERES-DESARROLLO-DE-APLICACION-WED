from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

from conexion.conexion import conectar_mysql
from models import Usuario

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-proyecto-tic"


# ==========================================================
# CONFIGURACIÓN FLASK-LOGIN
# ==========================================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


# ==========================================================
# CARGAR USUARIO DE LA SESIÓN
# ==========================================================

@login_manager.user_loader
def load_user(user_id):

    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, usuario FROM usuarios WHERE id = %s",
        (user_id,)
    )

    datos_usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if datos_usuario:
        return Usuario(
            datos_usuario["id"],
            datos_usuario["usuario"]
        )

    return None


# ==========================================================
# REGISTRO DE USUARIOS
# ==========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = conectar_mysql()
        cursor = conn.cursor(dictionary=True)

        # Comprobar si el usuario ya existe
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (form.usuario.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conn.close()

            flash(
                "Ese nombre de usuario ya está registrado.",
                "danger"
            )

            return render_template(
                "registro.html",
                form=form
            )

        # Proteger la contraseña mediante HASH
        password_hash = generate_password_hash(
            form.password.data
        )

        # Registrar usuario
        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Usuario registrado correctamente. Ahora puede iniciar sesión.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )


# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conn = conectar_mysql()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        datos_usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        # Comprobar contraseña protegida
        if datos_usuario and check_password_hash(
            datos_usuario["password"],
            form.password.data
        ):

            usuario = Usuario(
                datos_usuario["id"],
                datos_usuario["usuario"]
            )

            login_user(usuario)

            flash(
                "Inicio de sesión correcto.",
                "success"
            )

            return redirect(url_for("dashboard"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():

    titulo = "Sistema de Ingeniería TIC"
    mensaje = "Bienvenido al Proyecto Integrador"

    return render_template(
        "index.html",
        titulo=titulo,
        mensaje=mensaje
    )


# ==========================================================
# PRODUCTOS - LISTAR
# ==========================================================

@app.route("/productos")
@login_required
def productos():

    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_producto AS id,
            nombre,
            categoria,
            descripcion,
            precio,
            stock
        FROM productos
        ORDER BY id_producto DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==========================================================
# PRODUCTOS - ELIMINAR
# ==========================================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conn = conectar_mysql()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id_producto = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Producto eliminado correctamente.",
        "success"
    )

    return redirect(url_for("productos"))


# ==========================================================
# PRODUCTOS - NUEVO
# ==========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = conectar_mysql()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, categoria, descripcion, precio, stock)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.descripcion.data,
            float(form.precio.data),
            form.stock.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        # Vuelve al formulario vacío
        return redirect(url_for("nuevo_producto"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==========================================================
# PRODUCTOS - EDITAR
# ==========================================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    if producto is None:

        cursor.close()
        conn.close()

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(url_for("productos"))

    form = ProductoForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                descripcion = %s,
                precio = %s,
                stock = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.descripcion.data,
            float(form.precio.data),
            form.stock.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto actualizado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    # Cargar los datos actuales del producto
    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        editando=True
    )


# ==========================================================
# CLIENTES - LISTADO
# ==========================================================

@app.route("/clientes")
@login_required
def clientes():

    clientes = [
        {
            "nombre": "Universidad Estatal Amazónica",
            "correo": "contacto@uea.edu.ec",
            "telefono": "0990000001"
        },
        {
            "nombre": "Empresa Tecnológica Amazonía",
            "correo": "info@empresa.com",
            "telefono": "0990000002"
        },
        {
            "nombre": "Centro Educativo TIC",
            "correo": "info@centrotic.edu.ec",
            "telefono": "0990000003"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# ==========================================================
# CLIENTES - NUEVO
# ==========================================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "email": form.email.data,
            "telefono": form.telefono.data
        }

        print(cliente)

        return render_template(
            "formulario_cliente.html",
            form=form,
            mensaje="Cliente registrado correctamente."
        )

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ==========================================================
# PROVEEDORES - LISTADO
# ==========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    proveedores = [
        {
            "nombre": "Proveedor Tech Ecuador",
            "servicio": "Equipos informáticos",
            "contacto": "0991000001"
        },
        {
            "nombre": "Redes y Comunicaciones",
            "servicio": "Equipos de red",
            "contacto": "0991000002"
        },
        {
            "nombre": "Soluciones Digitales",
            "servicio": "Software y servicios tecnológicos",
            "contacto": "0991000003"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# ==========================================================
# PROVEEDORES - NUEVO
# ==========================================================

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "nombre": form.nombre.data,
            "empresa": form.empresa.data,
            "email": form.email.data,
            "telefono": form.telefono.data
        }

        print(proveedor)

        return render_template(
            "formulario_proveedor.html",
            form=form,
            mensaje="Proveedor registrado correctamente."
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================================
# FACTURACIÓN - LISTADO
# ==========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    facturas = [
        {
            "numero": "F001-001",
            "cliente": "Universidad Estatal Amazónica",
            "fecha": "15/08/2026",
            "total": 950.00,
            "estado": "Pagada"
        },
        {
            "numero": "F001-002",
            "cliente": "Empresa Tecnológica Amazonía",
            "fecha": "15/08/2026",
            "total": 1450.00,
            "estado": "Pendiente"
        },
        {
            "numero": "F001-003",
            "cliente": "Centro Educativo TIC",
            "fecha": "14/08/2026",
            "total": 95.00,
            "estado": "Pagada"
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# ==========================================================
# FACTURACIÓN - NUEVA
# ==========================================================

@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        factura = {
            "cliente": form.cliente.data,
            "producto": form.producto.data,
            "cantidad": form.cantidad.data,
            "total": float(form.total.data)
        }

        print(factura)

        return render_template(
            "formulario_facturacion.html",
            form=form,
            mensaje="Factura registrada correctamente."
        )

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)
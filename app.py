import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

from conexion.conexion import conectar_postgresql
from models import Usuario


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "clave-secreta-proyecto-tic"
)


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
    conn = conectar_postgresql()
    cursor = conn.cursor()

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
        conn = conectar_postgresql()
        cursor = conn.cursor()

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

        password_hash = generate_password_hash(form.password.data)

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
        conn = conectar_postgresql()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (
            form.usuario.data,
        ))

        datos_usuario = cursor.fetchone()

        cursor.close()
        conn.close()

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
    return render_template("dashboard.html")


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
# PRODUCTOS - LISTAR CON JOIN
# ==========================================================

@app.route("/productos")
@login_required
def productos():
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id_producto AS id,
            p.nombre,
            p.categoria,
            p.descripcion,
            p.precio,
            p.stock,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==========================================================
# PRODUCTOS - NUEVO
# ==========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()

    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    form.proveedor.choices = [
        (p["id_proveedor"], p["nombre"])
        for p in proveedores
    ]

    cursor.close()
    conn.close()

    if form.validate_on_submit():
        conn = conectar_postgresql()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (
                nombre,
                categoria,
                descripcion,
                precio,
                stock,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.descripcion.data,
            float(form.precio.data),
            form.stock.data,
            form.proveedor.data
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

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
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id_producto = %s
    """, (
        id,
    ))

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

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    form.proveedor.choices = [
        (p["id_proveedor"], p["nombre"])
        for p in proveedores
    ]

    if form.validate_on_submit():
        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                descripcion = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.descripcion.data,
            float(form.precio.data),
            form.stock.data,
            form.proveedor.data,
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

    if not form.is_submitted():
        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

        if producto["id_proveedor"] is not None:
            form.proveedor.data = producto["id_proveedor"]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        editando=True
    )


# ==========================================================
# PRODUCTOS - ELIMINAR
# ==========================================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    conn = conectar_postgresql()
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
# CLIENTES - LISTADO DEMOSTRATIVO
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
# CLIENTES - NUEVO DEMOSTRATIVO
# ==========================================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()

    if form.validate_on_submit():
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
# PROVEEDORES - LISTAR
# ==========================================================

@app.route("/proveedores")
@login_required
def proveedores():
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            empresa,
            email,
            telefono
        FROM proveedores
        ORDER BY id_proveedor DESC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

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
        conn = conectar_postgresql()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (
                nombre,
                empresa,
                email,
                telefono
            )
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.empresa.data,
            form.email.data,
            form.telefono.data
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================================
# PROVEEDORES - EDITAR
# ==========================================================

@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM proveedores
        WHERE id_proveedor = %s
    """, (
        id,
    ))

    proveedor = cursor.fetchone()

    if proveedor is None:
        cursor.close()
        conn.close()

        flash(
            "Proveedor no encontrado.",
            "danger"
        )

        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if form.validate_on_submit():
        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                empresa = %s,
                email = %s,
                telefono = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.empresa.data,
            form.email.data,
            form.telefono.data,
            id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash(
            "Proveedor actualizado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    if not form.is_submitted():
        form.nombre.data = proveedor["nombre"]
        form.empresa.data = proveedor["empresa"]
        form.email.data = proveedor["email"]
        form.telefono.data = proveedor["telefono"]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editando=True
    )


# ==========================================================
# PROVEEDORES - ELIMINAR
# ==========================================================

@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM proveedores WHERE id_proveedor = %s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(url_for("proveedores"))


# ==========================================================
# FACTURACIÓN - LISTAR CON JOIN
# ==========================================================

@app.route("/facturacion")
@login_required
def facturacion():
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            f.id_factura,
            f.cliente,
            f.cantidad,
            f.total,
            f.fecha,
            f.id_producto,
            p.nombre AS producto
        FROM facturas f
        INNER JOIN productos p
            ON f.id_producto = p.id_producto
        ORDER BY f.id_factura DESC
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

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

    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_producto, nombre
        FROM productos
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    form.producto.choices = [
        (p["id_producto"], p["nombre"])
        for p in productos
    ]

    cursor.close()
    conn.close()

    if form.validate_on_submit():
        conn = conectar_postgresql()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (
                cliente,
                id_producto,
                cantidad,
                total
            )
            VALUES (%s, %s, %s, %s)
        """, (
            form.cliente.data,
            form.producto.data,
            form.cantidad.data,
            float(form.total.data)
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================================
# FACTURACIÓN - EDITAR
# ==========================================================

@app.route("/facturacion/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_factura(id):
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM facturas
        WHERE id_factura = %s
    """, (
        id,
    ))

    factura = cursor.fetchone()

    if factura is None:
        cursor.close()
        conn.close()

        flash(
            "Factura no encontrada.",
            "danger"
        )

        return redirect(url_for("facturacion"))

    form = FacturacionForm()

    cursor.execute("""
        SELECT id_producto, nombre
        FROM productos
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    form.producto.choices = [
        (p["id_producto"], p["nombre"])
        for p in productos
    ]

    if form.validate_on_submit():
        cursor.execute("""
            UPDATE facturas
            SET cliente = %s,
                id_producto = %s,
                cantidad = %s,
                total = %s
            WHERE id_factura = %s
        """, (
            form.cliente.data,
            form.producto.data,
            form.cantidad.data,
            float(form.total.data),
            id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash(
            "Factura actualizada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    if not form.is_submitted():
        form.cliente.data = factura["cliente"]
        form.producto.data = factura["id_producto"]
        form.cantidad.data = factura["cantidad"]
        form.total.data = factura["total"]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_facturacion.html",
        form=form,
        editando=True
    )


# ==========================================================
# FACTURACIÓN - ELIMINAR
# ==========================================================

@app.route("/facturacion/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_factura(id):
    conn = conectar_postgresql()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM facturas WHERE id_factura = %s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash(
        "Factura eliminada correctamente.",
        "success"
    )

    return redirect(url_for("facturacion"))


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from conexion.conexion import conectar_mysql


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-proyecto-tic"


@app.route("/")
def inicio():
    titulo = "Sistema de Ingeniería TIC"
    mensaje = "Bienvenido al Proyecto Integrador"

    return render_template(
        "index.html",
        titulo=titulo,
        mensaje=mensaje
    )

@app.route("/productos")
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

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
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

    flash("Producto eliminado correctamente.", "success")

    return redirect(url_for("productos"))

@app.route("/productos/nuevo", methods=["GET", "POST"])
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

        flash("Producto registrado correctamente.", "success")

        return redirect(url_for("nuevo_producto"))

    return render_template(
        "formulario_producto.html",
        form=form
    )

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM productos WHERE id_producto = %s",
        (id,)

    )

    producto = cursor.fetchone()

    if producto is None:
        cursor.close()
        conn.close()
        flash("Producto no encontrado.", "danger")
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

        flash("Producto actualizado correctamente.", "success")

        return redirect(url_for("productos"))

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
    
@app.route("/clientes")
def clientes():
    clientes = [
        {"nombre": "Universidad Estatal Amazónica", "correo": "contacto@uea.edu.ec", "telefono": "0990000001"},
        {"nombre": "Empresa Tecnológica Amazonía", "correo": "info@empresa.com", "telefono": "0990000002"},
        {"nombre": "Centro Educativo TIC", "correo": "info@centrotic.edu.ec", "telefono": "0990000003"}
    ]
    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
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

@app.route("/proveedores")
def proveedores():
    proveedores = [
        {"nombre": "Proveedor Tech Ecuador", "servicio": "Equipos informáticos", "contacto": "0991000001"},
        {"nombre": "Redes y Comunicaciones", "servicio": "Equipos de red", "contacto": "0991000002"},
        {"nombre": "Soluciones Digitales", "servicio": "Software y servicios tecnológicos", "contacto": "0991000003"}
    ]
    return render_template("proveedores.html", proveedores=proveedores)

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
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

@app.route("/facturacion")
def facturacion():
    facturas = [
        {"numero": "F001-001", "cliente": "Universidad Estatal Amazónica", "fecha": "15/08/2026", "total": 950.00, "estado": "Pagada"},
        {"numero": "F001-002", "cliente": "Empresa Tecnológica Amazonía", "fecha": "15/08/2026", "total": 1450.00, "estado": "Pendiente"},
        {"numero": "F001-003", "cliente": "Centro Educativo TIC", "fecha": "14/08/2026", "total": 95.00, "estado": "Pagada"}
    ]
    return render_template("facturacion.html", facturas=facturas)
@app.route("/facturacion/nueva", methods=["GET", "POST"])
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



if __name__ == "__main__":
    app.run(debug=True)

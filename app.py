from flask import Flask, render_template
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

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
    productos = [
        {"nombre": "Computador portátil", "categoria": "Hardware", "descripcion": "Equipo para desarrollo de software y actividades académicas.", "precio": 850.00, "stock": 10},
        {"nombre": "Router Wi-Fi", "categoria": "Redes", "descripcion": "Dispositivo para conectividad y administración de redes.", "precio": 95.00, "stock": 7},
        {"nombre": "Servidor", "categoria": "Infraestructura", "descripcion": "Equipo destinado a servicios y almacenamiento de información.", "precio": 1450.00, "stock": 0}
    ]
    return render_template("productos.html", productos=productos)
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()

    if form.validate_on_submit():
        producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "descripcion": form.descripcion.data,
            "precio": float(form.precio.data),
            "stock": form.stock.data
        }

        print(producto)

        return render_template(
            "formulario_producto.html",
            form=form,
            mensaje="Producto registrado correctamente."
        )

    return render_template(
        "formulario_producto.html",
        form=form
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

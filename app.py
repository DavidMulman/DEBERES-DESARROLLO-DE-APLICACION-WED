from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/clientes")
def clientes():
    clientes = [
        {"nombre": "Universidad Estatal Amazónica", "correo": "contacto@uea.edu.ec", "telefono": "0990000001"},
        {"nombre": "Empresa Tecnológica Amazonía", "correo": "info@empresa.com", "telefono": "0990000002"},
        {"nombre": "Centro Educativo TIC", "correo": "info@centrotic.edu.ec", "telefono": "0990000003"}
    ]
    return render_template("clientes.html", clientes=clientes)

@app.route("/proveedores")
def proveedores():
    proveedores = [
        {"nombre": "Proveedor Tech Ecuador", "servicio": "Equipos informáticos", "contacto": "0991000001"},
        {"nombre": "Redes y Comunicaciones", "servicio": "Equipos de red", "contacto": "0991000002"},
        {"nombre": "Soluciones Digitales", "servicio": "Software y servicios tecnológicos", "contacto": "0991000003"}
    ]
    return render_template("proveedores.html", proveedores=proveedores)

@app.route("/facturacion")
def facturacion():
    facturas = [
        {"numero": "F001-001", "cliente": "Universidad Estatal Amazónica", "fecha": "15/08/2026", "total": 950.00, "estado": "Pagada"},
        {"numero": "F001-002", "cliente": "Empresa Tecnológica Amazonía", "fecha": "15/08/2026", "total": 1450.00, "estado": "Pendiente"},
        {"numero": "F001-003", "cliente": "Centro Educativo TIC", "fecha": "14/08/2026", "total": 95.00, "estado": "Pagada"}
    ]
    return render_template("facturacion.html", facturas=facturas)

if __name__ == "__main__":
    app.run(debug=True)

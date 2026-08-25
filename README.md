# Proyecto Integrador U3 - Avance 9/16

## Ingeniería en Tecnologías de la Información y Comunicación

Proyecto web desarrollado con HTML5, CSS3, Bootstrap, JavaScript, Python y Flask.

### Estructura

- `app.py`: aplicación Flask y rutas.
- `templates/base.html`: plantilla base con herencia Jinja2.
- `templates/index.html`: página principal.
- `templates/productos.html`: módulo Productos.
- `templates/clientes.html`: módulo Clientes.
- `templates/proveedores.html`: módulo Proveedores.
- `templates/facturacion.html`: módulo Facturación.
- `static/css/style.css`: estilos.
- `static/js/script.js`: validaciones y registros dinámicos.
- `static/img/`: imágenes del proyecto.

## Ejecución local

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
pip install flask
python app.py
```

Abrir:

http://127.0.0.1:5000/

Rutas:

- `/`
- `/productos`
- `/clientes`
- `/proveedores`
- `/facturacion`

No se utiliza base de datos en esta semana; los módulos utilizan datos demostrativos.

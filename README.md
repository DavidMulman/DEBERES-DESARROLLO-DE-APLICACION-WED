# Proyecto Integrador U3 - Avance 11/16

## Ingeniería en Tecnologías de la Información y Comunicación

Proyecto web desarrollado con HTML5, CSS3, Bootstrap, JavaScript, Python, Flask, Jinja2, Flask-WTF y WTForms.

## Estructura

- `app.py`: aplicación Flask, rutas y procesamiento de formularios.
- `forms/__init__.py`: inicialización del módulo de formularios.
- `forms/producto_form.py`: formulario y validaciones de productos.
- `forms/cliente_form.py`: formulario y validaciones de clientes.
- `forms/proveedor_form.py`: formulario y validaciones de proveedores.
- `forms/facturacion_form.py`: formulario y validaciones de facturación.
- `templates/base.html`: plantilla base con herencia Jinja2.
- `templates/index.html`: página principal.
- `templates/productos.html`: módulo Productos.
- `templates/clientes.html`: módulo Clientes.
- `templates/proveedores.html`: módulo Proveedores.
- `templates/facturacion.html`: módulo Facturación.
- `templates/formulario_producto.html`: formulario de productos.
- `templates/formulario_cliente.html`: formulario de clientes.
- `templates/formulario_proveedor.html`: formulario de proveedores.
- `templates/formulario_facturacion.html`: formulario de facturación.
- `templates/components/navbar.html`: barra de navegación reutilizable.
- `templates/components/footer.html`: pie de página reutilizable.
- `static/css/style.css`: estilos del proyecto.
- `static/js/script.js`: funcionalidades JavaScript.
- `static/img/`: imágenes del proyecto.

## Funcionalidades implementadas

- Uso de Flask y Jinja2.
- Herencia de plantillas mediante `base.html`.
- Reutilización de componentes con `navbar.html` y `footer.html`.
- Contenido dinámico con listas y diccionarios de Python.
- Bucles `{% for %}` y condicionales `{% if %}`.
- Formularios con Flask-WTF y WTForms.
- Validación de campos obligatorios con `DataRequired()`.
- Validación de longitud con `Length()`.
- Validación de correos electrónicos con `Email()`.
- Validación de valores numéricos con `NumberRange()`.
- Uso de métodos GET y POST.
- Procesamiento mediante `form.validate_on_submit()`.
- Protección CSRF mediante `form.hidden_tag()`.
- Configuración de `SECRET_KEY`.
- Mensajes de error debajo de cada campo.
- Formularios para productos, clientes, proveedores y facturación.

## Ejecución local

Crear el entorno virtual:

```bash
python -m venv venv

### Windows

```bash
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir:

http://127.0.0.1:5000/ 

Rutas:

- `/`
- `/productos`
- `/productos/nuevo`
- `/clientes`
- `/clientes/nuevo`
- `/proveedores`
- `/proveedores/nuevo`
- `/facturacion`
v/facturacion/nueva`

No se utiliza base de datos en esta semana; los módulos utilizan datos demostrativos.

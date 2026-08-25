from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):
    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(message="El cliente es obligatorio."),
            Length(min=3, max=100, message="El nombre del cliente debe tener entre 3 y 100 caracteres.")
        ]
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(message="El producto es obligatorio."),
            Length(min=3, max=100, message="El nombre del producto debe tener entre 3 y 100 caracteres.")
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(min=1, message="La cantidad debe ser mayor que 0.")
        ]
    )

    total = DecimalField(
        "Total",
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(min=0.01, message="El total debe ser mayor que 0.")
        ]
    )

    submit = SubmitField("Guardar factura")
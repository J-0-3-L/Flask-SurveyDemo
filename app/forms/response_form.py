from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField

class ResponseForm(FlaskForm):
    # Define las opciones del formulario como RadioField
    selected_option = RadioField('Selecciona una opción', choices=[], coerce=int)
    submit = SubmitField('Guardar Respuesta')


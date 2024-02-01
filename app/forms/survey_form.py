from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

class CreateSurveyForm(FlaskForm):
    title = StringField("Título de la encuesta", validators=[DataRequired()])
    description = TextAreaField("Descripción de la encuesta")
    submit = SubmitField("siguiente")

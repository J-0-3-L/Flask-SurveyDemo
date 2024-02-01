from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, FormField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class SurveyQuestionForm(FlaskForm):
    question_text = StringField("Pregunta", validators=[DataRequired()])
    options_per_question = FieldList(StringField("Opción"))
    survey_id = HiddenField()  # Agrega el campo oculto survey_id
    submit = SubmitField("Crear")

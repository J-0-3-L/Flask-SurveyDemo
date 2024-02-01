from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class QuestionOptionForm(FlaskForm):
    option_text = StringField("Opcion", validators=[DataRequired()])
    question_id = HiddenField()
    submit = SubmitField("Añadir")
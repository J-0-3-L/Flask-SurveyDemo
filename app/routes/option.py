from flask import Blueprint, render_template, url_for, flash, redirect, request

from app import db
from app.models.option import Option
from app.models.question import Question
from app.forms.option_form import QuestionOptionForm

from flask_login import current_user, login_required

option_bp = Blueprint("option", __name__)

@option_bp.route("/option/<int:question_id>", methods=['GET', 'POST'])
def createOption(question_id):

    form = QuestionOptionForm()
    question = Question.query.get(question_id)

    if request.method == 'POST' and form.validate_on_submit():
        option_text = form.option_text.data
        # selected_option = request.form.get('selected_option')

        option = Option(option_text=option_text, question=question)
        db.session.add(option)
        db.session.commit()

        flash("Se ha añadido una opcion a la pregunta")
        return redirect(url_for("question.createQuestion", survey_id=question.survey.id))
    
    form.question_id.data = question_id
    options = Option.query.filter_by(question_id=question_id).all()

    return render_template("survey/option.html", form=form, options=options)
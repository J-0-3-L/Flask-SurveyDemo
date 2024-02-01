from flask import Blueprint, render_template, url_for, flash, redirect, request

from app import db
from app.models.question import Question
from app.models.survey import Survey
from app.forms.question_form import SurveyQuestionForm

from flask_login import current_user, login_required

question_bp = Blueprint("question", __name__)

@question_bp.route("/question/<int:survey_id>", methods=['GET','POST'])
def createQuestion(survey_id):

    form = SurveyQuestionForm()
    survey = Survey.query.get(survey_id)

    if request.method == 'POST' and form.validate_on_submit():
        question_text = form.question_text.data

        question = Question(question_text=question_text, survey=survey)
        db.session.add(question)
        db.session.commit()
        

        flash("Se ha creado una nueva pregunta")
        return redirect(url_for("question.createQuestion",survey_id=survey_id))

    form.survey_id.data = survey_id
    questions = Question.query.filter_by(survey_id=survey_id).all()
    
    return render_template("survey/question.html", form=form, questions=questions)
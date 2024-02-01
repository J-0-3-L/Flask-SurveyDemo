from flask import Blueprint, render_template, url_for, flash, request , redirect

from flask_login import current_user,login_required

from app import db
from app.models.survey import Survey
from app.models.question import Question
from app.models.option import Option
from app.forms.survey_form import CreateSurveyForm
from app.forms.response_form import ResponseForm

survey_bp = Blueprint("survey", __name__)

# CREAR
@survey_bp.route("/createSurvey", methods=["POST", "GET"])
def createSurvey():
    form = CreateSurveyForm()

    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        user_id = current_user.id

        new_survey = Survey(title=title, description=description, user_id=user_id)
        db.session.add(new_survey)
        db.session.commit()

        survey_id = new_survey.id

        flash("Se ha creado la encuesta")
        return redirect(url_for("question.createQuestion", survey_id=new_survey.id))

    return render_template("survey/survey.html", form=form)

# EDITAR
@survey_bp.route("/updateSurvey/<id>", methods=['GET', 'POST'])
def updateSurvey(id):
    survey = Survey.query.get(id)

    question = Question.query.get(id)
    option = Option.query.get(id)

    if request.method == 'POST':
        survey.title = request.form["title"]
        survey.description = request.form['description']

        question.question_text = request.form["question_text"]
        option.option_text = request.form["option_text"]

        db.session.commit()
        return redirect(url_for("admin.dash"))

    flash("Se actualizo la encuesta")
    return render_template("updateSurvey.html", survey=survey , question=question, option=option)

# DELETE
@survey_bp.route("/deleteSurvey/<id>", methods=['GET'])
def deleteSurvey(id):
    survey = Survey.query.get(id)

    db.session.delete(survey)
    db.session.commit()
    flash("Se elimino correctamente la encuesta")
    return redirect(url_for("admin.dash"))


# VER POR ID
@survey_bp.route("/viewSurvey/<int:survey_id>", methods=['GET'])
@login_required
def viewSurvey(survey_id):
    survey = Survey.query.get(survey_id)
    questions = Question.query.filter_by(survey_id=survey.id).all()
    options = {}

    for question in questions:
        options[question.id] = Option.query.filter_by(question_id=question.id).all()

    return render_template("survey/viewSurvey.html", survey=survey, questions=questions, options=options)

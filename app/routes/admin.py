from flask import Blueprint, url_for, flash, redirect, render_template, request

from flask_login import current_user, login_required

from app import db
from app.models.survey import Survey
from app.models.user import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/admin')
@login_required
def dash():
    surveys = Survey.query.all()
    users = User.query.all()
    return render_template("main.html", surveys=surveys, users=users)
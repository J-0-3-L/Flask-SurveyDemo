from flask import Blueprint, render_template, url_for, flash, redirect, current_app, request

from app import db, login_manager, bcrypt, http_auth, jwt

from flask_login import current_user, login_user, logout_user, login_required
from app.models.user import User
from app.forms.signup_form import SignupForm
from app.forms.login_form import LoginForm
from werkzeug.utils import secure_filename


auth_bp = Blueprint("auth", __name__)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@http_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash("debe iniciar usuario")
    return redirect(url_for("auth.login"))

# @auth_bp.route("/")
# def authView():
#     return "hola a todos en las encuestas"

@auth_bp.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dash"))
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.lower()
        email = form.email.data.lower()
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            user = User(
                username=username,
                email=email
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("El usuario se creó correctamente")
            return redirect(url_for('auth.login'))
        else:
            flash("Ya existe un usuario con ese username")
    return render_template("auth/signup.html", form=form)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dash"))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("¡Bienvenido!")
            return redirect(url_for('admin.dash'))
        else:
            flash("Revisa tus credenciales")
    return render_template("auth/signin.html", form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/editar/<id>",methods=['GET','POST'])
def edit(id):
    form = SignupForm()
    user = User.query.get(id)
    if request.method == 'POST' and form.validate_on_submit():
        if user.id == current_user.id:
            user.username = form.username.data
            # user.password = form.password.data
            user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash("Se ha actualizado tu usuario con exito!")
            return redirect(url_for('auth.login'))
        else:
            flash("No puedes modificar el usuario")
    form.username.data = user.username
    form.password.data = user.password_hash
    return render_template("auth/signup.html" , form=form)

# @auth_bp.route("/delete/<id>", methods=['GET'])
# def erase(id):
#     user = User.query.get(id)
#     if user and user.id == current_user.id:
#         posts = Post.query.filter_by(user_id=user.id).all()
#         for post in posts:
#             db.session.delete(post)
#         db.session.delete(user)
#         db.session.commit()
#         flash("Se ha eliminado el usuario y sus posts satisfactoriamente!")
#     else:
#         flash("El usuario no existe o no tiene permisos para eliminarlo")
#     return redirect(url_for("views_bp.users"))
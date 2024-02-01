from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from config import Config

from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
bcrypt = Bcrypt()
http_auth = HTTPBasicAuth()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.routes.auth import auth_bp as auth
        from app.routes.survey import survey_bp as survey
        from app.routes.question import question_bp as question
        from app.routes.option import option_bp as option

        from app.routes.admin import admin_bp as admin

        app.register_blueprint(auth)
        app.register_blueprint(survey)
        app.register_blueprint(question)
        app.register_blueprint(option)

        app.register_blueprint(admin)
        
        db.create_all()
    return app

from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib


class User(db.Model, UserMixin):
    __tablename__='users'
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False )
    password_hash= db.Column(db.String(255), nullable=False)
    surveys = db.relationship('Survey', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


#     def set_avatar(self, size=100, default="identicon", rating="g"):
#         url = "https://secure.gravatar.com/avatar"
#         hash = hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()
#         self.avatar_url = f"{url}/{hash}?s={size}&d={default}&r={rating}"
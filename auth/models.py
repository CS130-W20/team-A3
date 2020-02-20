"""
models.py
====================
Define the models for user authorization (anonymous user and normal user)
"""
from __init__ import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class AnonymousUser(AnonymousUserMixin):
    @staticmethod
    def get_name():
        return None

    @staticmethod
    def get_id():
        return -1

    @staticmethod
    def is_active():
        return False

    @staticmethod
    def is_anonymous():
        return True

class User(UserMixin, db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    email = db.Column(db.String(255))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))

    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    interests = db.Column(db.String(500))
    education = db.Column(db.String(100))

    user_since = db.Column(db.DateTime(), default=db.func.current_timestamp())
    verified = db.Column(db.Boolean(), default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_verified(self):
        return self.verified

    def get_name(self):
        return self.username

    def get_email(self):
        return self.email

    def get_education(self):
        return self.education

    def get_date_created(self):
        return self.date_created

    def get_date_modified(self):
        return self.date_modified

    def get_interests(self):
        return self.interests
        
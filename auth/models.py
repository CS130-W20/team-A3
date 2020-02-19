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
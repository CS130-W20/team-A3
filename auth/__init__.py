"""
__init__.py
====================
The initialization file for the auth module
"""
from auth.models import AnonymousUser, User
from __init__ import login_manager

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




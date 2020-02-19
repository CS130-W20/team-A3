from flask import Flask, render_template, g, request, session, url_for, redirect
from flask_login import current_user, LoginManager
import json

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Define the WSGI application object
application = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(application)






@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Configurations
application.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(application)

# Import a module / component using its blueprint handler variable (mod_auth)
#from auth.controllers import auth
from search.controllers import searcher
from users.controllers import users
from visualization.controllers import visualizer

# Register blueprint(s)
#application.register_blueprint(auth)
application.register_blueprint(searcher)
application.register_blueprint(users)
application.register_blueprint(visualizer)

# handeling the category selection



@application.before_request
def before_request():
    g.user = current_user

@application.route('/', methods=['GET', 'POST'])
def main():
    """
        Default landing page.

    :return: HTML Template for the landing page.
    """



# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
from flask import Flask, render_template, g, session
from flask_login import current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
import json


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

# Get course taxonomy
from browse.generate_categories import generate_course_list
browse_categories = generate_course_list("browse/course_taxonomy.txt")
#Get concept_dict
with open("visualization/concept_hierarchy.json",'r') as load_f:
    concept_dict = json.load(load_f)

# Import a module / component using its blueprint handler variable (mod_auth)
from auth.controllers import auth
from search.controllers import searcher
from users.controllers import users
from visualization.controllers import visualizer
from browse.controllers import browse,get_category_info


# Register blueprint(s)
application.register_blueprint(auth)
application.register_blueprint(searcher)
application.register_blueprint(users)
application.register_blueprint(visualizer)
application.register_blueprint(browse)




@application.before_request
def before_request():
    g.user = current_user

@application.route('/', methods=['GET', 'POST'])
def main():
    """
        Default landing page.

    :return: HTML Template for the landing page.
    """
    if session.get("current_category") is None:
        session["current_category"] = get_category_info(-1)
    return render_template('search.html', nonempty=True, welcome=True, browse_categories=browse_categories)



# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

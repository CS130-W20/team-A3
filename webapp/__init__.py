from flask import Flask, render_template, g, request, session, url_for, redirect
from flask_login import current_user, LoginManager
import json

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Define the WSGI application object
application = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(application)

browse_categories = [
        {'id': 0, 'category_name': 'Artificial Intelligence',
         'sub_categories': [
             {'id': 1, 'category_name': 'Machine Learning', 'sub_categories': []},
             {'id': 2, 'category_name': 'Knowledge Engineering', 'sub_categories': [
                 {'id': 3, 'category_name': 'category 1.2.1', 'sub_categories': []},
                 {'id': 4, 'category_name': 'category 1.2.2', 'sub_categories': []}
             ]},
             {'id': 5, 'category_name': 'Deep Learning', 'sub_categories': []}
         ]
         },
        {'id': 6, 'category_name': 'Information Security', 'sub_categories': []},
        {'id': 7, 'category_name': 'Database',
         'sub_categories': [
             {'id': 8, 'category_name': 'Database Application and Development', 'sub_categories': [
                 {'id': 12, 'category_name': 'category 3.1.1', 'sub_categories': []}
             ]},
             {'id': 9, 'category_name': 'Data Model', 'sub_categories': [
                 {'id': 10, 'category_name': 'category 3.2.1', 'sub_categories': []},
                 {'id': 11, 'category_name': 'category 3.2.2', 'sub_categories': []}
             ]}
         ]
         },
        {'id': 13, 'category_name': 'Computer Theory Science', 'sub_categories': []},
        {'id': 14, 'category_name': 'Information Security', 'sub_categories': []},
        {'id': 15, 'category_name': 'Software System', 'sub_categories': []},
        {'id': 16, 'category_name': 'Network and data communication', 'sub_categories': []},
        {'id': 17, 'category_name': 'Computer interdisciplinary', 'sub_categories': []},
        {'id': 18, 'category_name': 'Computer Architecture', 'sub_categories': []},
        {'id': 19, 'category_name': 'Computer Application', 'sub_categories': []},
        {'id': 20, 'category_name': 'Computer Hardware', 'sub_categories': []},
        {'id': 21, 'category_name': 'Software Engineering', 'sub_categories': []},
        {'id': 22, 'category_name': 'General Theory', 'sub_categories': []}
    ]


def include_category_tree(tmp_tree, tmp_dict):
    for child in tmp_tree:
        tmp_dict[child["id"]] = child["category_name"]
        sub_categories = child.get("sub_categories", [])
        if len(sub_categories):
            tmp_dict = include_category_tree(sub_categories, tmp_dict)
    return tmp_dict

id2categories = include_category_tree(browse_categories, {-1: "Welcome to Education AI"})

def get_category_introduction(category_id=-1):
    '''
    this is fake now, please implement it later
    '''
    if category_id == -1:
        introduction = "We will help you get started with AI and enjoy your study."
    else:
        introduction = "brief introduction of category {}: {}".format(category_id, id2categories[category_id])
    return introduction

def get_category_content(category_id=-1):
    '''
    this is all fake, please implement it later
    '''
    if category_id == -1:
        content = [
            {   "title": "Hot Topics", 
                "content": ["We have some keywords for you that are recently very popular:",
                    [
                        "Machine Learning",
                        "Artificial Intelligence",
                        "Data Mining",
                        "Big Data"
                    ]
                ],
                "link": "#"
            },
            {   "title": "Popular Resource", 
                "content": ["Here are some of the courses / blogs that are recently very popular on our dataset. (balabalabala)"
                ],
                "link": "#"
            },
            {   "title": "What\'s New", 
                "content": ["Here are some of the recently-come-out courses... (balabalabala)"
                ],
                "link": "#"
            }
        ]
    else:
        category_name = id2categories[category_id]
        content = [
            {   "title": "Related Topics", 
                "content": ["balabalabalabala"
                ]
            },
            {   "title": "Brief History", 
                "content": ["The development of {} experienced the following main stages".format(category_name),
                    [
                        {"stage 1": "#"},
                        {"stage 2": "#"},
                        {"stage 3": "#"},
                        {"stage 4": "#"}
                    ]
                ],
                "link": "#"
            },
            {   "title": "Most Recent Paper", 
                "content": ["Here are some of the most-recent research papers in {}... (balabalabala)".format(category_name)
                ],
                "link": "#"
            }
        ]
    return content

def get_category_info(category_id):
    category_intro = get_category_introduction(category_id)
    category_name = id2categories[category_id]
    category_content = get_category_content(category_id)
    category_info = {"id": category_id, "name": category_name, "intro": category_intro, "content": category_content}
    return category_info


@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Configurations
application.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(application)

# Import a module / component using its blueprint handler variable (mod_auth)
from auth.controllers import auth
from search.controllers import searcher
from users.controllers import users
from visualization.controllers import visualizer

# Register blueprint(s)
application.register_blueprint(auth)
application.register_blueprint(searcher)
application.register_blueprint(users)
application.register_blueprint(visualizer)

# handeling the category selection
@application.route('/select_category', methods=['POST'])
def select_category():
    jsondata = request.form.get('data')
    data = json.loads(jsondata)
    # Notice: this category id is turned to string after passing back from the front-end
    category_id = int(data["category_id"])
    if category_id == -1:
        print("TODO: category selection is canceled, please do something to clear the selection in the backend")
    else:
        print("TODO: category {} selected, please do something to implement browse mode".format(category_id))
    session["current_category"] = get_category_info(category_id)
    success = 1
    info = [{
        "success": success,
        "current_category": session["current_category"]
    }]
    return json.dumps(info)


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
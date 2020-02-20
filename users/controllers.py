from users.__init__ import *
from auth import load_user
from users.modules.history import get_user_history
from users.modules.recommendation import recommend_course_for_user
from users.modules.education import get_education_options
from users.modules.interests import get_interests_options
from users.modules.portfolio import get_user_description, get_user_photo, remove_previous_image
import sqlite3

from flask import request, redirect

from __init__ import application as app

users = Blueprint('user', __name__)

@users.route('/home/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    '''
    Updates user profile picture.

    Modal sends POST request with image to this function, which saves the
    image to the server with name [user id].[extension].
    '''
    user_id = current_user.get_id()
    direct_to = '/home/' + user_id

    f = request.files['photo']
    filename = "{}.{}".format(user_id, f.filename.split(".")[-1])

    remove_previous_image(user_id, app.config["UPLOAD_FOLDER"])
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    print(filename)

    return redirect("/home/"+user_id)

@users.route('/home/update_info', methods=['GET', 'POST'])
def update_info():
    '''
    Updates user information

    HTML sends POST request with new information, which this function writes
    to the database.
    '''
    user_id = current_user.get_id()
    direct_to = '/home/' + user_id

    username = request.form.get('printUserName')
    email    = request.form.get('email')
    edulevel = request.form.get('inputEduLevel')

    conn = sqlite3.connect(USERDB_PATH)
    conn.execute('''
        UPDATE user
        SET
            date_modified = datetime('now'),
            email = ?,
            education = ?
        WHERE id = ?
    ''', (email, edulevel, user_id))
    conn.commit()

    return redirect("/home/"+user_id)

@users.route('/home/update_description', methods=['GET', 'POST'])
def update_description():
    '''
    Updates user description text by clicking 'Update button'.

    Clicking 'Update' button sends POST to this function with text value of
    the description text area. Function then writes this description to the
    database.
    '''
    user_id = current_user.get_id()
    direct_to = '/home/' + user_id

    new_desc = request.form.get('new_desc')

    conn = sqlite3.connect(USERDB_PATH)
    conn.execute('''
        UPDATE user_description
        SET description = ?
        WHERE id = ?
    ''', (new_desc, user_id))
    conn.commit()

    return redirect("/home/"+user_id)

@users.route('/user_data_vis/<user_id>', methods=['GET', 'POST'])
@users.route('/user_data_vis/<user_id>/<visualize_mode>/', methods=['GET', 'POST'])
@users.route('/user_data_vis/<user_id>/<visualize_mode>', methods=['GET', 'POST'])
def user_visualize(user_id=None, visualize_mode="0", methods=['GET', 'POST']):
    welcome_page = redirect(url_for("main"))

@users.route('/home', methods=['GET', 'POST'])
@users.route('/home/<user_id>/', methods=['GET', 'POST'])
@users.route('/home/<user_id>', methods=['GET', 'POST'])
def user_home(user_id=None):
    '''
    Builds user page.

    Calls on different users modules to create a user page where users can
    get course recommendations, see their footprint, and change their info.
    '''
    welcome_page = redirect(url_for("main"))

    authorized = False
    if user_id is None or user_id == -1:
        return welcome_page

    current_user_id = current_user.get_id()
    authorized = current_user_id==user_id

    try:
        show_user = load_user(user_id)
        if show_user.get_id() == -1 or not show_user.is_verified():
            return welcome_page
        g.show_user = show_user
    except:
        return welcome_page
    g.user_history = get_user_history(user_id)
    g.user_recommend = recommend_course_for_user(user_id)
    g.education_levels = get_education_options()
    g.user_description = get_user_description(user_id)
    g.user_image = get_user_photo(user_id, app.config["UPLOAD_FOLDER"])
    g.interests = get_interests_options()
    return render_template('home.html', authorized=authorized)

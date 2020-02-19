import json
import datetime
import random
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from __init__ import db, login_manager

from flask_login import current_user, login_user, logout_user, login_required
# Import module models (i.e. User)
from auth.models import User

# Define the blueprint: 'auth'
auth = Blueprint('auth', __name__)

def chatbot(text):
    print("TODO: we should do something to handle the chat message; a chatbot. currently it is fake.")
    success = 1 # fail: 0
    candidate_answers = ["hi!", "Hummmmm...", "Yes you are right!", "Yes I totally agree with you!", "Pardon me?", "That sounds interesting!"]
    # not using if text.lower().find("name") != -1 anymore
    words_mentioned = set(text.lower().split())
    if "name" in words_mentioned or "who" in words_mentioned:
        reply_text = "I am Eda (Education AI) from UCLA! Nice to meet you!"
    elif "you" in words_mentioned or "eda" in words_mentioned:
        reply_text = "I am just the first version of a chatbot; let's not talk about me, let's talk more about you!"
    elif "hello" in words_mentioned or "hi" in words_mentioned or "greeting" in words_mentioned:
        reply_text = "How dost thou, sweet lord?"
    elif "ai" in words_mentioned or "ml" in words_mentioned or "dm" in words_mentioned \
        or "machine learning" in words_mentioned or "artificial intelligence" in words_mentioned or "data mining" in words_mentioned:
        reply_text = "Yes you got it! I am an expert in the fields you mentioned. But currently I don't know how to organize my words to tell you what I know."
    else:
        reply_text = random.sample(candidate_answers, 1)[0]
    return success, reply_text

@auth.route('/chatbot_handle', methods=['POST'])
def chatbot_handle():
    jsondata = request.form.get('data')
    data = json.loads(jsondata)
    text = data["text"]
    success, reply_text = chatbot(text)
    if success == 0:
        success = 1
        reply_text = "Sorry I can't understand what are you talking about."
    info = [{
            "success": success,
            "reply": reply_text
        }
    ]
    return json.dumps(info)

# handeling the category selection
@auth.route('/select_category', methods=['POST'])
def select_category():
    jsondata = request.form.get('data')
    data = json.loads(jsondata)
    category_id = data["category_id"]
    if category_id == "-1":
        print("TODO: category selection is canceled, please do something to clear the selection in the backend")
    else:
        print("TODO: category {} selected, please do something to implement browse mode".format(category_id))
    print("Notice: this category id is turned to string after passing back from the front-end")
    success = 1
    info = [{
        "success": success
    }
    ]
    return json.dumps(info)


# Set the route and accepted methods
@auth.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        flash('You\'re already logged in!')
        return redirect('/')

    to_register = len(request.form.get('reg', '')) > 0
    print(to_register)
    if to_register:
        print("Redirecting.")
        return redirect('/register', code=307)

    username = request.form.get('username', '')
    password = request.form.get('password', '')


    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None or not check_password_hash(registered_user.password, password):
        # flash('Username or Password is invalid', 'error')
        # return (json.dumps([{'success':0,'message':'Invalid credentials'}]), 204)
        # TODO - I haven't find a way to smoothly solve this issue:
        #      how to use ajax to report this error message?
        #      So, for now, I simply did smooth
        error = "The user name and password does not match, or the user hasn't registered yet."
        return redirect(url_for('main', error=error))
    login_user(registered_user)
    flash('Logged in successfully')
    session['user'] = registered_user.id
    return redirect(request.args.get('next') or '/')

@login_required
@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect('/')


@auth.route('/emailcheck', methods=['POST'])
def check_email_exists():
    user = User.query.filter_by(email=request.form['email'])
    if user:
        return json.dumps({'success': False, "code": 1, "message": "Email unavailable"})
    return json.dumps({'success': True, 'code': 0})


@auth.route('/usernamecheck', methods=['POST'])
def check_username_exists():
    username=json.loads(request.form['data'])['username']
    user = User.query.filter_by(username=username).first()

    if user:
        return json.dumps([{'success': 0, "code": 1, "message": "Username unavailable"}])
    return json.dumps([{'success': 1, 'code': 0}])


@auth.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '')
    password = generate_password_hash(request.form.get('password', ''))
    user = User.query.filter_by(username=username).first()

    if user:
        return json.dumps([{'success':0, "code": 1, "message":"Username unavailable"}])
    try:
        user = User(
                username=username,
                password=password,
                user_since=datetime.datetime.now()
                    )
        db.session.add(user)
        db.session.commit()
        login_user(user)
    except:
        # return json.dumps([{'success':0, "code" : 1, "message":"Database error"}])
        error = "registration was not successful, please try again later or contact our team"
        return redirect(url_for('main', error=error))
    return redirect('/newuser')


@login_required
@auth.route('/newuser', methods=['GET','POST'])
def new_user():
    if request.method == 'GET':
        if current_user.is_anonymous:
            redirect('/')
        else:
            username = current_user.username
            if current_user.verified:
                redirect('/')
            else:
                return render_template('first_time_login.html', username=username)

    if request.method == 'POST':
        f_name = request.form['inputFirstname']
        l_name = request.form['inputLastname']
        education = request.form['inputEduLevel']
        email = request.form['inputEmail']
        user = User.query.filter_by(id=current_user.id).first()
        user.fname = f_name
        user.lname = l_name
        user.email = email
        user.verified = True
        user.education = education
        interests = request.form.getlist('inputInterests')
        concepts = request.form.getlist('inputConcepts')

        # new user interests entry in interests table should be populated according to questionnaire
        # temporarily initialize to interests + random bool
        interests = (current_user.id, ) + tuple(interests) + tuple(np.random.randint(0, 2, 100 - len(interests), 'bool'))
        # new user knowledge entry in knowledge table should be populated according to questionnaire
        # temporarily initialize to interests + random bool
        concepts = (current_user.id, ) + tuple(concepts) + tuple(np.random.randint(0, 2, 100 - len(concepts), 'bool'))

        try:
            db.session.add(user)
            db.session.execute("INSERT INTO interests VALUES (%s)" % ",".join(['?' for i in range(101)]), interests)
            db.session.execute("INSERT INTO knowledge VALUES (%s)" % ",".join(['?' for i in range(101)]), concepts)
            db.session.commit()
        except:
            return render_template('500.html'),\
                                    json.dumps({'success': False, "code": 1, "message": "Database error"})

    return redirect('/')

"""
controllers.py
====================
Controller for auth module
"""

import json
import datetime
import random
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
# https://stackoverflow.com/questions/15473626/make-a-post-request-while-redirecting-in-flask

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from __init__ import db, login_manager

from flask_login import current_user, login_user, logout_user, login_required
# Import module models (i.e. User)
from auth.models import User

import sqlite3
import numpy as np
from users import USERDB_PATH 

# Define the blueprint: 'auth'
auth = Blueprint('auth', __name__)


# Set the route and accepted methods
@auth.route('/login', methods=['POST'])
def login():
    direct_to = request.referrer or '/'
    # print(request.referrer, "**************")
    if current_user.is_authenticated:
        flash('You\'re already logged in!')
        return redirect(direct_to, code=307)

    to_register = len(request.form.get('reg', '')) > 0
    # print(to_register)
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
        flash(error, 'error')
        return redirect(direct_to, code=307)
    login_user(registered_user)
    flash('Logged in successfully', 'message')
    session['user'] = registered_user.id
    return redirect(request.args.get('next') or direct_to, code=307)

#handle log out
@login_required
@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    direct_to = request.referrer or '/'
    logout_user()
    flash('Logged out successfully!', 'message')
    return redirect(direct_to, code=307)

#handle email check
@auth.route('/emailcheck', methods=['POST'])
def check_email_exists():
    user = User.query.filter_by(email=request.form['email'])
    if user:
        return json.dumps({'success': False, "code": 1, "message": "Email unavailable"})
    return json.dumps({'success': True, 'code': 0})

#handle user name check
@auth.route('/usernamecheck', methods=['POST'])
def check_username_exists():
    username=json.loads(request.form['data'])['username']
    user = User.query.filter_by(username=username).first()

    if user:
        return json.dumps([{'success': 0, "code": 1, "message": "Username unavailable"}])
    return json.dumps([{'success': 1, 'code': 0}])

#handle register
@auth.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '')
    password = generate_password_hash(request.form.get('password', ''))
    user = User.query.filter_by(username=username).first()

    if user:
        return json.dumps([{'success':0, "code": 1, "message":"Username {} unavailable".format(username)}])
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

#newuser information collection
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
        interests = request.form.getlist('inputInterests')
        concepts = request.form.getlist('inputConcepts')



        education = request.form['inputEduLevel']
        email = request.form['inputEmail']
        user = User.query.filter_by(id=current_user.id).first()
        user.fname = f_name
        user.lname = l_name
        user.email = email
        user.verified = True
        #temporarily save interests in user also to keep consistency
        user.interests = ",".join(interests)
        user.education = education

        # new user interests entry in interests table should be populated according to questionnaire
        # temporarily initialize to interests + random bool
        interests = (current_user.id, ) + tuple(interests) + tuple(np.random.randint(0, 2, 100 - len(interests), 'bool'))

        # new user knowledge entry in knowledge table should be populated according to questionnaire
        # temporarily initialize to concepts + random bool
        concepts = (current_user.id, ) + tuple(concepts) + tuple(np.random.randint(0, 2, 100 - len(concepts), 'bool'))

        try:
            db.session.add(user)
            db.session.commit()
            conn = sqlite3.connect(USERDB_PATH)
            cur = conn.cursor()            
            cur.execute("INSERT INTO interests VALUES (%s)" % ",".join(['?' for i in range(101)]), interests)
            cur.execute("INSERT INTO knowledge VALUES (%s)" % ",".join(['?' for i in range(101)]), concepts)
            conn.commit()
            conn.close()
        except:
            return render_template('500.html'),\
                                    json.dumps({'success': False, "code": 1, "message": "Database error"})

    return redirect('/')
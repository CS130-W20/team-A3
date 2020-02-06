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

from werkzeug.utils import secure_filename

import os
import json
import datetime
import random
import configparser
import os

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from __init__ import db, login_manager
from flask_login import current_user, login_user, logout_user, login_required

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')
USERDB_PATH = config['DEFAULT']['user_db_path']
CONFIG_PATH = 'config.ini'

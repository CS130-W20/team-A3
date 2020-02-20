import os
from flask import url_for
import sqlite3
import pandas as pd
from users import USERDB_PATH   # path to users db

def get_user_description(user_id):
    '''
    Returns a user's custom description stored in the database

    Parameters:
    user_id (int): ID of user

    Returns:
    string: user description
    '''

    conn = sqlite3.connect(USERDB_PATH)
    desc = pd.read_sql_query("SELECT description FROM user_description WHERE id=%s" % user_id, conn).iloc[0][0]
    return desc

def get_user_photo(user_id, user_imgs_path):
    '''
    Returns the name of the profile image for a user based on user ID

    Parameters:
    user_id (int): ID of user
    user_imgs_path (string): path to directory of user images

    Returns:
    string: Name of user image file
    '''

    all_imgs_names = os.listdir(user_imgs_path)

    file_name = "default.jpg"
    for img_name in all_imgs_names:
        img_id = img_name.split('.')[0]
        if len(img_id) and str(img_id) == str(user_id):
            file_name = img_name

    return file_name

def remove_previous_image(user_id, user_imgs_path):
    '''
    Removes a user image file from the server

    Parameters:
    user_id (int): ID of user
    user_imgs_path (string): path to directory of user images
    '''

    all_imgs_names = os.listdir(user_imgs_path)
    for img_name in all_imgs_names:
        img_id = img_name.split('.')[0]
        if len(img_id) and str(img_id) == str(user_id):
            os.remove(os.path.join(user_imgs_path, img_name))

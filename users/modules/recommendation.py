import sqlite3
import pandas as pd
import numpy as np
from users import USERDB_PATH   # path to users db
from search import COURSEDB_PATH  # path to courses db

'''DELETE ME '''
import pickle
import re

def recommend_course_for_user(user_id):
    """
    Returns name and link to courses to recommend to a specific user.

    Connects to user_interest, user_knowledge, and course_concepts tables
    and uses the vector representations of each to find courses which a user may
    be interested in (course covers many user interests) as well as matches
    background of user (user has background knowledge to complete course).

    Parameters:
    user_id (int): ID of user

    Returns:
    array: Names and links to courses
    """
    # get user knowledge and interests
    conn = sqlite3.connect(USERDB_PATH)
    userinfo_df =   pd.read_sql_query("SELECT * FROM user      WHERE id=%s"      % user_id, conn).iloc[0]
    knowledge =     pd.read_sql_query("SELECT * FROM knowledge WHERE user_id=%s" % user_id, conn).iloc[0][1:]
    interests =     pd.read_sql_query("SELECT * FROM interests WHERE user_id=%s" % user_id, conn).iloc[0][1:]

    # print(pd.read_sql_query("SELECT id, fname, lname FROM user", conn, index_col='id'))
    # print(pd.read_sql_query("SELECT * FROM knowledge", conn, index_col='user_id'))
    # print(pd.read_sql_query("SELECT * FROM interests", conn, index_col='user_id'))

    # get course embeddings
    conn = sqlite3.connect(COURSEDB_PATH)
    courses_df = pd.read_sql_query("SELECT * FROM course_concepts", conn, index_col='course_id')

    conn.close()

    # print(knowledge)
    # print(interests)
    # print(courses_df)

    recommended = [
        {"name": "Machine Learning: Classification", "link": "/search/Coursera_99/"},
        {"name": "Machine Learning: Regression", "link": "/search/Coursera_83/"},
        {"name": "Mathematics for Machine Learning: PCA", "link": "/search/Coursera_91/"}
    ]
    return recommended

import sqlite3
import pandas as pd
import numpy as np
from users import USERDB_PATH   # path to users db
from search import COURSEDB_PATH  # path to courses db
import re

def get_user_history(user_id):
    """
    Returns name and link to courses to recommend to a specific user based on
    user knowledge.

    Connects to user_knowledge and course_concepts tables
    and uses the vector representations of each to find courses which a user
    already has backgroun in and may be interested in reviewing.

    Parameters:
    user_id (int): ID of user

    Returns:
    array: Names and links to courses
    """
    # get user knowledge and interests
    conn = sqlite3.connect(USERDB_PATH)
    knowledge =     pd.read_sql_query("SELECT * FROM knowledge WHERE user_id=%s" % user_id, conn).iloc[0][1:]

    # get course embeddings
    conn = sqlite3.connect(COURSEDB_PATH)
    courses_df = pd.read_sql_query("SELECT * FROM course_concepts", conn, index_col='course_id')
    conn.close()

    recs = courses_df.mul(np.array(knowledge), axis=1).sum(axis=1).sort_values(ascending=False).index

    recommended = []
    for rec in recs[:5]:
        rex = re.compile(r'<course_name>(.*?)</course_name>')
        f = open('database/data_courses/%s' % rec, 'r')
        course_name = rex.search(f.read()).group(1)
        course_name = course_name.replace("&amp;", "&")
        course_link = "/search/" + rec[:-4] + "/"
        recommended += [{"name": course_name, "link": course_link}]
        f.close()

    return recommended

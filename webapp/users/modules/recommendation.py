import sqlite3
import pandas as pd
import numpy as np
from users import USERDB_PATH   # path to users db
from search import COURSEDB_PATH  # path to courses db

def recommend_course_for_user(user_id):

    # get user knowledge and interests
    conn = sqlite3.connect(USERDB_PATH)
    userinfo_df =   pd.read_sql_query("SELECT * FROM user      WHERE id=%s"      % user_id, conn).iloc[0]
    knowledge =     pd.read_sql_query("SELECT * FROM knowledge WHERE user_id=%s" % user_id, conn).iloc[0][1:]
    interests =     pd.read_sql_query("SELECT * FROM interests WHERE user_id=%s" % user_id, conn).iloc[0][1:]

    # need to do some reorganizing of bytes after recovering entries from database
    knowledge = np.array([x[0] for x in knowledge])
    interests = np.array([x[0] for x in interests])

    # print(pd.read_sql_query("SELECT id, fname, lname FROM user", conn))
    # print(pd.read_sql_query("SELECT * FROM knowledge", conn))
    # print(pd.read_sql_query("SELECT * FROM interests", conn))

    # get course embeddings
    conn = sqlite3.connect(COURSEDB_PATH)
    courses_df = pd.read_sql_query("SELECT * FROM course_concepts", conn, index_col='course_id')
    for i, col in enumerate(courses_df.columns):
        courses_df[col] = [x[0] for x in courses_df[col]]

    conn.close()

    # print(knowledge)
    # print(interests)
    # print(courses_df)

    print("WARNING from users.modules.recommendation: This function is FAKE now, please do something to handle the user's history in the future")
    recommended = [
        {"name": "Machine Learning: Classification", "link": "/search/Coursera_99/"},
        {"name": "Machine Learning: Regression", "link": "/search/Coursera_83/"},
        {"name": "Mathematics for Machine Learning: PCA", "link": "/search/Coursera_91/"}
    ]
    return recommended

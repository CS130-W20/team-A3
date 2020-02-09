import sqlite3
import pandas as pd

from users import USERDB_PATH   # path to users db
from search import POSTDB_PATH     # path to courses db

def recommend_course_for_user(user_id):

    # get user knowledge and interests
    conn = sqlite3.connect(USERDB_PATH)
    df = pd.read_sql_query("SELECT * FROM user WHERE id=%s" % user_id, conn)
    conn.close()

    # print(df)

    # get course embeddings
    conn = sqlite3.connect(POSTDB_PATH)
    df = pd.read_sql_query("SELECT * FROM postings", conn)
    conn.close()

    # print(df)


    print("WARNING from users.modules.recommendation: This function is FAKE now, please do something to handle the user's history in the future")
    recommended = [
        {"name": "Machine Learning: Classification", "link": "/search/Coursera_99/"},
        {"name": "Machine Learning: Regression", "link": "/search/Coursera_83/"},
        {"name": "Mathematics for Machine Learning: PCA", "link": "/search/Coursera_91/"}
    ]
    return recommended

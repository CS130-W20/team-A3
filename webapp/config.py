import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Statement for enabling the development environment
DEBUG = True

# Define the database URIs

COURSES_DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'courses.db')
USERS_DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'users.db')

SQLALCHEMY_BINDS = {
    'users': USERS_DB_URI
}

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2


# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = b"ty985692t82g9#@*$98958387r3t3519"

# Secret key for signing cookies
SECRET_KEY = b"6298nyygt(TQ$65639Q01503968p(*^#%#()@$!#"
USERNAME = 'admin'
PASSWORD = 'default'

UPLOAD_FOLDER = "./static/img/users/"
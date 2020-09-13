import os

from dotenv import load_dotenv

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SOURCE_DIR, '.env')
load_dotenv(dotenv_path=ENV_PATH, verbose=True)

POSTGRES ={
    "user": os.getenv("POSTGRES_USER", "monitoring_admin"),
    "pw": os.getenv("POSTGRES_PASSWORD", "password"),
    "db": os.getenv("POSTGRES_DB", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", 5432)
}

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
SQL_ALCHEMY_ECHO = True

WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT", 5000)

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Create in-memory database
#DATABASE_FILE = 'sample_db.sqlite'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
#SQLALCHEMY_ECHO = True

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

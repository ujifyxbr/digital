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

LEARNING_FOLDER = 'learning'
MONITORING_FOLDER = 'monitoring'

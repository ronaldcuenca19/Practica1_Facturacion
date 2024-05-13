from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, '.env'))

class Config:
    # Configuración GENERAL
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Configuracion de BDD
    user = environ.get('MYSQL_USER')
    password = environ.get('MYSQL_PASSWORD')
    host = environ.get('MYSQL_HOST')
    db = environ.get('MYSQL_DATABASE')

    SECRET_KEY = environ.get("SECRET_KEY")

    # CONFIGURACION DE LA SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f'mysql://{user}:{password}@{host}/{db}'
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = 'enable'

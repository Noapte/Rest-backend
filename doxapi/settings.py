import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "dummy")
DOCUMENTS_DATABASE_URI = os.environ.get("DOCUMENTS_DATABASE_URI")
DOXAPI_SETTINGS = os.environ.get("DOXAPI_SETTINGS", "Local")

assert DOXAPI_SETTINGS in ("Production", "Test", "Local", "Docker")

if DOXAPI_SETTINGS == "Production":
    assert DOCUMENTS_DATABASE_URI

CURRENT_CONFIG = "{}.{}".format(__name__, DOXAPI_SETTINGS)


class Config:

    DEBUG = False
    TESTING = False

    SECRET_KEY = SECRET_KEY or "dummy"
    SECURITY_PASSWORD_SALT = "salt"
    SECURITY_POST_LOGIN_VIEW = "/admin"
    SECURITY_POST_LOGOUT_VIEW = "/login"

    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ERROR_404_HELP = False

    JWT_HEADER_TYPE = ""
    JWT_ERROR_MESSAGE_KEY = "message"
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_REFRESH_TOKEN_EXPIRES = False

    DOCUMENTS_VERSION = "1.5.0"


class Production(Config):

    SQLALCHEMY_DATABASE_URI = DOCUMENTS_DATABASE_URI


class Test(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class Development(Config):

    DEBUG = True


class Local(Development):

    SQLALCHEMY_DATABASE_URI = "postgresql://doxapi:doxapi@localhost:5432/doxapi"


class Docker(Development):

    SQLALCHEMY_DATABASE_URI = "postgresql://doxapi:doxapi@postgres:5432/doxapi"

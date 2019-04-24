from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from doxapi.settings import CURRENT_CONFIG

app = Flask(__name__)
app.config.from_object(CURRENT_CONFIG)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

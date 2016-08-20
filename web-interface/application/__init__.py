from json import load
import os.path

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

with open(os.path.join(
        os.path.dirname(__file__), 'arcrank-config.json'), 'r') as f:

    config = load(f)

app = Flask(__name__)

APP_SETTINGS = 'application.settings'
app.config.from_object(APP_SETTINGS)

db = SQLAlchemy(app)

db.create_all()
db.session.commit()

from . import views

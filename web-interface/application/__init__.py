from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

APP_SETTINGS = 'application.settings'
app.config.from_object(APP_SETTINGS)

db = SQLAlchemy(app)

db.create_all()
db.session.commit()

from . import views

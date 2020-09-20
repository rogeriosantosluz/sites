import os
import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import get_config

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

app.config['SECRET_KEY'] = get_config("SECRET_KEY")
app.config['ADMIN_USERNAME'] = get_config("ADMIN_USERNAME")
app.config['ADMIN_PASSWORD'] = get_config("ADMIN_PASSWORD")

Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir+"/db", 'sites.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import *
db.create_all()
db.session.commit()

app.logger.info('App inicializada')
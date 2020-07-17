"""
This is the central file that serves as the Handler for the app (Factory Pattern)

Bootstrap is not invoked as custom Bootstrap resources are used by the html files so far.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from datetime import timedelta
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Add upload security 
    #app.config.from_object(config["ALLOWED_IMAGE_EXTENSIONS"])
    #app.config.from_object(config["MAX_IMAGE_FILESIZE"])
      
    #bootstrap.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Define session duration
    app.permanent_session_lifetime = timedelta(minutes=5)

    return app
from flask import Flask
from .config import ConfigDev
from .extensions import db, csrf, limiter, security
from .models.models import User, Role
from flask_security import SQLAlchemyUserDatastore

def create_app(config_class=ConfigDev):
    app = Flask(__name__)
    app.config.from_object(config_class)


    # inicializa as extensoes do extensions.py
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # configuração do Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)  

    @app.route("/")
    def index():
        return "Hello World!"
    
    return app
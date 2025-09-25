from flask import Flask
from .config import ConfigDev
from .extensions import db, csrf, limiter

def create_app(config_class=ConfigDev):
    app = Flask(__name__)
    app.config.from_object(config_class)


    # inicializa as extensoes do extensions.py
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    @app.route("/")
    def index():
        return "Hello World!"
    
    return app
from flask import Flask
from .config import ConfigDev
from .extensions import db, csrf, limiter, security
from .models.models import User, Role
from flask_security import SQLAlchemyUserDatastore
from src.auth.datastore import user_datastore  
from src.auth import init_app as init_auth
from src.usuario.usuarios import usuarios_bp

from src.admin.admin import admins_bp


def create_app(config_class=ConfigDev):
    app = Flask(__name__)
    app.config.from_object(config_class)


    # inicializa as extensoes do extensions.py
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # configuração do Flask-Security
    security.init_app(app, user_datastore)

    # registra os blueprints
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(admins_bp)

    # inicializa o modulo de autenticação
    init_auth(app)

    # Cria todas as tabelas do banco de dados automaticamente
    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return "Hello World!"
    
    return app
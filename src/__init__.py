from flask import Flask, app, render_template, redirect, url_for
from .config import ConfigDev
from .extensions import db, csrf, limiter, security
from .models.models import User, Role
from flask_security import SQLAlchemyUserDatastore, LoginForm
from flask_security.utils import verify_and_update_password
from src.auth.datastore import user_datastore  
from src.auth import init_app as init_auth
from src.user.users import users_bp
from .auth import auth
from src.admin.admin import admins_bp

def create_app(config_class=ConfigDev):
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(config_class)

    # inicializa as extensoes do extensions.py
    db.init_app(app)
    csrf.init_app(app)
    # limiter.init_app(app)

    # configuração do Flask-Security
    security.init_app(app, user_datastore)

    # registra os blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(admins_bp)

    # inicializa o modulo de autenticação
    auth.init_app(app)

    # Cria todas as tabelas do banco de dados automaticamente
    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.route("/")
    def index():
        form = LoginForm()
        return render_template('security/login_user.html', login_user_form=form)
        # descomente essa linha caso nao seja necessario logar para acessar a pagina inicial
        # return render_template('index.html')
        

    @app.route("/home")
    def home():
        return render_template('index.html')
    return app
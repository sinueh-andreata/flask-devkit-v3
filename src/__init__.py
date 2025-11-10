from flask import Flask, app, render_template, redirect, url_for
from .config import ConfigDev
from .extensions import db, csrf, limiter, security
from .models.models import User, Role, create_default_roles, create_default_users
from flask_security import SQLAlchemyUserDatastore, LoginForm
from flask_security.utils import verify_and_update_password
from src.auth.datastore import user_datastore  
from src.auth import init_app as init_auth
from src.routes.users import users_bp as users_bp
from src.api.users import users_bp as users_api_bp
from src.routes.admin import admin_bp as admin_bp
from src.api.admin import admin_bp as admin_api_bp
from src.routes.root import root_bp as root_bp
from src.api.root import root_bp as root_api_bp


from .auth import auth

def create_app(config_class=ConfigDev):
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(config_class)

    # inicializa as extensoes do extensions.py
    db.init_app(app)
    csrf.init_app(app)

    # configuração do Flask-Security
    security.init_app(app, user_datastore)

    # registra os blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(users_api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_api_bp)
    app.register_blueprint(root_bp)
    app.register_blueprint(root_api_bp)
    # inicializa o modulo de autenticação
    auth.init_app(app)

    # Cria todas as tabelas do banco de dados automaticamente
    with app.app_context():
        db.create_all()
        create_default_roles()
        create_default_users()

    @app.route("/")
    def index():
        form = LoginForm()
        return render_template('security/login_user.html', login_user_form=form)
        # descomente essa linha caso nao seja necessario logar para acessar a pagina inicial
        # return render_template('index.html')
        
    @app.route("/home")
    def home():
        return render_template('home.html')
    return app
from flask import Flask, app, render_template, redirect, url_for
from .config import ConfigDev
from .extensions import db, csrf, limiter, security
from .models.models import User, Role
from flask_security import SQLAlchemyUserDatastore
from flask_security.forms import LoginForm, RegisterForm
from flask_security.utils import verify_and_update_password
from src.auth.datastore import user_datastore  
from src.auth import init_app as init_auth
from src.usuario.usuarios import usuarios_bp
from .auth import auth
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
        return render_template('index.html')
    
    @app.route('/entrar', methods=['GET', 'POST'])
    def entrar():
        form = LoginForm()
        if form.validate_on_submit():

            pass
        return render_template('security/login.html', form=form)

    @app.route('/cadastrar', methods=['GET', 'POST'])
    def cadastrar():
        form = RegisterForm()
        if form.validate_on_submit():
            # criar usuário manualmente ou usar user_datastore.create_user
            pass
        return render_template('security/register.html', form=form)

    return app
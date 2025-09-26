from flask import Flask, render_template
from .config import ConfigDev
from .extensions import db, csrf, limiter, security
from .models.models import User, Role
from flask_security import SQLAlchemyUserDatastore
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
    security.init_app(app, user_datastore,
                    register_form=None,
                    login_form=None
                    )

    # registra os blueprints
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(admins_bp)

    # inicializa o modulo de autenticação
    auth.init_app(app)

    # Cria todas as tabelas do banco de dados automaticamente
    with app.app_context():
        db.create_all()
        
        if not Role.query.filter_by(name='usuario').first():
            usuario_role = Role(name='usuario', description='Usuário padrão')
            db.session.add(usuario_role)
        db.session.commit()
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.route("/")
    def index():
        return render_template('index.html')

    return app
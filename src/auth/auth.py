from flask import Blueprint, render_template, redirect, request, url_for
from flask_security import user_registered
from ..extensions import csrf
from flask_wtf.csrf import generate_csrf
from ..extensions import db
from ..models.models import Role

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return {'csrf_token': token}

def on_user_registered(sender, user, **extra):
    default_role = Role.query.filter_by(name="user").first()
    if default_role:
        user.roles.append(default_role)
        db.session.commit()

def init_app(app):
    user_registered.connect(on_user_registered, app)
    app.register_blueprint(auth_bp)
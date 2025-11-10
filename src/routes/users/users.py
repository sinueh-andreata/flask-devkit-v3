from flask import Blueprint, render_template
from flask_security import login_required
from flask_security.decorators import roles_accepted, current_user
from . import users_bp

@users_bp.route("/", methods=['GET'])
@login_required
@roles_accepted('user', 'admin', 'root')
def home_users():
    return render_template("users_templates/home.html", message="Bem-vindo", username=current_user.username)
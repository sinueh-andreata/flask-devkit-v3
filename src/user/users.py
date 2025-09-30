from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_security.decorators import roles_required, current_user
from flask_security.forms import LoginForm, RegisterForm

users_bp = Blueprint('users', __name__)

@users_bp.route("/rtuser")
@login_required
@roles_required('user')
def minha_rota():
    if not current_user.has_role('user'):
        return jsonify({"message": "Acesso negado: você não tem a role necessária"}), 403
    return jsonify({"message": "Apenas usuários autenticados veem isso"})


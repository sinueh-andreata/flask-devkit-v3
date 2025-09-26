from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for
from flask_security.decorators import roles_required, current_user

admins_bp = Blueprint('admins', __name__)

@admins_bp.route("/rtadmin")
@login_required
@roles_required('admin')
def minha_rota():
    if not current_user.has_role('admin'):
        return jsonify({"message": "Acesso negado: você não tem a role necessária"}), 403
    return jsonify({"message": "Apenas administradores autenticados veem isso"})
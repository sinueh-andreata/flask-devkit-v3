from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for
from flask_security.decorators import roles_required, current_user

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route("/rtuser")
@login_required
@roles_required('usuario')
def minha_rota():
    if not current_user.has_role('usuario'):
        return jsonify({"message": "Acesso negado: você não tem a role necessária"}), 403
    return jsonify({"message": "Apenas usuários autenticados veem isso"})
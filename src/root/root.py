from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for
from flask_security.decorators import roles_required, current_user

root_bp = Blueprint('root', __name__)

@root_bp.route("/rtroot")
@login_required
@roles_required('root')
def minha_rota():
    if not current_user.has_role('root'):
        return jsonify({"message": "Acesso negado: você não tem a role necessária"}), 403
    return jsonify({"message": "Apenas root autenticados veem isso"})


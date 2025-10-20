from flask_security import login_required
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_security.decorators import roles_required, current_user

root_bp = Blueprint('root', __name__, url_prefix='/root')

@root_bp.route("/rtroot")
@login_required
@roles_required('root')
def minha_rota():
    if not current_user.has_role('root'):
        return jsonify({"message": "Acesso negado: você não tem a role necessária"}), 403
    return jsonify({"message": "Apenas root autenticados veem isso"})

@root_bp.route("/")
@login_required
@roles_required('root') 
def root_home():
    return render_template('root_templates/home.html')





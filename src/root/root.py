from flask_security import login_required
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_security.decorators import roles_required, current_user
from ..models.models import User
from ..auth.datastore import user_datastore
from datetime import datetime

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



@root_bp.route("/create/users/admin", methods=['POST'])
@login_required
@roles_required('root')
def create_admin_user():
    if not current_user.has_role('root'):
        return jsonify({"message": "Acesso negado: você não tem a role necessária"}), 403

    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e password são obrigatórios'}), 400

    existing_user = user_datastore.find_user(email=email)
    if existing_user:
        return jsonify({'error': 'Usuário com este email já existe'}), 400

    try:
        user_datastore.create_user(email=email, password=password)
        user_datastore.add_role_to_user(email, 'admin')
        user_datastore.add_role_to_user(email, 'user')

        fs_uniquifier = user_datastore.find_user(email=email).fs_uniquifier
        user = user_datastore.find_user(fs_uniquifier=fs_uniquifier)
        user.active = True
        user.confirmed_at = datetime.utcnow()
        user_datastore.commit()
        return jsonify({'message': f'Usuário admin {email} criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_security.decorators import roles_required, current_user
from ..models.models import Produto

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

def get_all_produtos():
    try:
        produtos = Produto.query.order_by(Produto.nome).all()
        return produtos
    except Exception:
        raise

@produtos_bp.route('/', methods=['GET'])
@login_required
@roles_required('root')
def listar_produtos():
    try:
        produtos = get_all_produtos()
        return jsonify([p.to_dict() for p in produtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
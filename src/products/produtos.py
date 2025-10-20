from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_security.decorators import roles_required, roles_accepted, current_user
from ..models.models import Produto
from ..extensions import db
import re

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/')
def pagina_produtos():

    all_products = get_all_produtos()

    return render_template('produtos/produtos.html')

@produtos_bp.route('/all/products', methods=['GET'])
def get_all_produtos():
    try:
        produtos = Produto.query.order_by(Produto.nome).all()
        return jsonify([p.to_dict() for p in produtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@produtos_bp.route('/produto/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/novo/produto', methods=['POST'])
@login_required
@roles_accepted('admin', 'root')
def criar_produto():
    data = request.get_json(silent=True) or {}
    nome = data.get('nome')
    preco = data.get('preco')
    estoque = data.get('estoque')

    if not nome or preco is None or estoque is None:
        return jsonify({'error': 'Nome, preço e estoque são obrigatórios'}), 400

    if nome and not re.match(r'^[a-zA-Z\s]*$', nome):
        return jsonify({'error': 'Nome do produto inválido. Apenas letras e espaços são permitidos.'}), 400

    try:
        preco = float(preco)
        estoque = int(estoque)
    except (ValueError, TypeError):
        return jsonify({'error': 'Preço deve ser número e estoque deve ser inteiro.'}), 400

    if preco < 0:
        return jsonify({'error': 'Preço não pode ser negativo.'}), 400

    if estoque < 0:
        return jsonify({'error': 'Estoque não pode ser negativo.'}), 400

    try:
        novo_produto = Produto(nome=nome, preco=preco, estoque=estoque)
        db.session.add(novo_produto)
        db.session.commit()
        return jsonify(novo_produto.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@produtos_bp.route('/atualizar/produto/<int:produto_id>', methods=['PUT'])
@login_required
@roles_required('admin')
def atualizar_produto(produto_id):
    data = request.get_json(silent=True) or {}
    nome = data.get('nome')
    preco = data.get('preco')
    estoque = data.get('estoque')

    if nome and not re.match(r'^[a-zA-Z\s]*$', nome):
        return jsonify({'error': 'Nome do produto inválido. Apenas letras e espaços são permitidos.'}), 400

    try:
        preco = float(preco)
        estoque = int(estoque)
    except (ValueError, TypeError):
        return jsonify({'error': 'Preço deve ser número e estoque deve ser inteiro.'}), 400

    if preco < 0:
        return jsonify({'error': 'Preço não pode ser negativo.'}), 400

    if estoque < 0:
        return jsonify({'error': 'Estoque não pode ser negativo.'}), 400

    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404

        produto.nome = nome
        produto.preco = preco
        produto.estoque = estoque
        db.session.commit()
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@produtos_bp.route('/deletar/produto/<int:produto_id>', methods=['DELETE'])
@login_required
@roles_required('admin')
def deletar_produto(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404

        db.session.delete(produto)
        db.session.commit()
        return jsonify({'message': 'Produto deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
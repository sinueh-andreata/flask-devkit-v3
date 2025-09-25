from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route("/rtuser")
@login_required
def minha_rota():
    return jsonify({"message": "Apenas usuários autenticados veem isso"})
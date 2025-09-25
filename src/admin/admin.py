from flask_security import login_required, roles_required
from flask import Blueprint, jsonify, request, redirect, url_for

admins_bp = Blueprint('admins', __name__)

@admins_bp.route("/rtadmins")
@roles_required('admin')
def rota_admins():
    return jsonify({"message": "Apenas administradores veem isso"})
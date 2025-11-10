from flask import Blueprint

users_bp = Blueprint('users_api', __name__, url_prefix='/api/users')
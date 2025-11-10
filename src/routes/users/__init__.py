from flask import Blueprint

users_bp = Blueprint('users_routes', __name__, url_prefix='/users')
from flask import Blueprint

products_bp = Blueprint('products_routes', __name__, url_prefix='/products')
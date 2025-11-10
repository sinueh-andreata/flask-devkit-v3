from flask import Blueprint

products_bp = Blueprint('products_api', __name__, url_prefix='/api/products')
from flask import render_template, Blueprint

erros_bp = Blueprint('errors', __name__, url_prefix='/errors')


@erros_bp.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@erros_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
from flask_security import login_required
from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_security.decorators import roles_required, current_user
from flask_security.forms import LoginForm, RegisterForm

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route("/rtuser")
@login_required
@roles_required('usuario')
def minha_rota():
    if not current_user.has_role('usuario'):
        return jsonify({"message": "Acesso negado: você não tem a role necessária"}), 403
    return jsonify({"message": "Apenas usuários autenticados veem isso"})

@usuarios_bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('security/login.html', form=form)

@usuarios_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('security/register.html', form=form)
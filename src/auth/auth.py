from flask import Blueprint, render_template, redirect, request, url_for

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return "Login Page"
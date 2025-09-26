from flask import Blueprint, render_template, redirect, request, url_for
from flask_security import user_registered
from ..extensions import db
from ..models.models import Role

def on_user_registered(sender, user):
    default_role = Role.query.filter_by(name="usuario").first()
    if default_role:
        user.roles.append(default_role)
        db.session.commit()

def init_app(app):
    user_registered.connect(on_user_registered, app)

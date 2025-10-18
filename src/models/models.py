from datetime import datetime
import uuid
from flask_security import UserMixin, RoleMixin
from ..extensions import db, Security
from argon2 import PasswordHasher

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Produto {self.nome}>'

def create_default_roles():
    default_roles = ['admin', 'user', 'root']
    for role_name in default_roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()

def create_default_users():
    ph = PasswordHasher()

    default_users = [
        {
            # users
            'email': 'user@mail.com',
            'password': 'user123',
            'active': True,
            'confirmed_at': datetime.utcnow(),
            'fs_uniquifier': str(uuid.uuid4()),
            'roles': ['user']
        },
        {
            # admins
            'email': 'admin@mail.com',
            'password': 'admin123',
            'active': True,
            'confirmed_at': datetime.utcnow(),
            'fs_uniquifier': str(uuid.uuid4()),
            'roles': ['admin']
        },
        {
            # roots
            'email': 'root@mail.com',
            'password': 'root123',
            'active': True,
            'confirmed_at': datetime.utcnow(),
            'fs_uniquifier': str(uuid.uuid4()),
            'roles': ['root']
        }
    ]

    create_default_roles()
    for u in default_users:
        existing_user = User.query.filter_by(email=u['email']).first()
        if existing_user:
            continue

        hashed_password = ph.hash(u['password'])

        user = User(
            email=u['email'],
            password=hashed_password,
            active=u.get('active', True),
            confirmed_at=u.get('confirmed_at', datetime.utcnow()),
            fs_uniquifier=u.get('fs_uniquifier', str(uuid.uuid4()))
        )

        for role_name in u.get('roles', []):
            role = Role.query.filter_by(name=role_name).first()
            if role:
                user.roles.append(role)

        db.session.add(user)

    db.session.commit()

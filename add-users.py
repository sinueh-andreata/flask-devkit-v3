# Script para adicionar usuários e roles padrão ao banco de dados

from src import admin, create_app
from src.extensions import db
from src.auth.datastore import user_datastore
from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

app = create_app()

with app.app_context():
    if not user_datastore.find_role("admin"):
        user_datastore.create_role(name="admin", description="Administrador")
        db.session.commit()

    email = "adminrs@admin.com"
    password = "senha-1234"
    hashed_password = hash_password(password)
    if not user_datastore.find_user(email=email):
        user = user_datastore.create_user(email=email, password=hashed_password, active=True)
        db.session.commit()
    else:
        user = user_datastore.find_user(email=email)

    if "admin" not in [role.name for role in user.roles]:
        user_datastore.add_role_to_user(user, "admin")
        db.session.commit()

    print("Admin criado e role atribuída!")

    if not user_datastore.find_role("user"):
        user_datastore.create_role(name="user", description="Usuário padrão")
        db.session.commit()

    email = "userrs@user.com"
    password = "senha-1234"
    hashed_password = hash_password(password)
    if not user_datastore.find_user(email=email):
        user = user_datastore.create_user(email=email, password=hashed_password, active=True)
        db.session.commit()
    else:
        user = user_datastore.find_user(email=email)

    if "user" not in [role.name for role in user.roles]:
        user_datastore.add_role_to_user(user, "user")
        db.session.commit()

    print("Usuário criado e role atribuída!")
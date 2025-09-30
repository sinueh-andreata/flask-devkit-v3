# Script para adicionar usuários e roles ao banco de dados
# Para descomentar tudo use Ctrl + ; ou Ctrl + Shift + K + U
# Ou simplemente delete esse arquivo

from src import create_app
from src.extensions import db
from src.auth.datastore import admin_datastore, user_datastore

app = create_app()

with app.app_context():
    if not admin_datastore.find_role("admin"):
        admin_datastore.create_role(name="admin", description="Administrador")
        db.session.commit()

    email = "admin@admin.com"
    password = "senha-123"
    if not admin_datastore.find_user(email=email):
        admin = admin_datastore.create_user(email=email, password=password, active=True)
        db.session.commit()
    else:
        admin = admin_datastore.find_user(email=email)

    if "admin" not in [role.name for role in admin.roles]:
        admin_datastore.add_role_to_user(admin, "admin")
        db.session.commit()

    print("Admin criado e role atribuída!")

    if not user_datastore.find_role("user"):
        user_datastore.create_role(name="user", description="Usuário padrão")
        db.session.commit()

    email = "user@user.com"
    password = "senha-123"
    if not user_datastore.find_user(email=email):
        user = user_datastore.create_user(email=email, password=password, active=True)
        db.session.commit()
    else:
        user = user_datastore.find_user(email=email)

    if "user" not in [role.name for role in user.roles]:
        user_datastore.add_role_to_user(user, "user")
        db.session.commit()

    print("Usuário criado e role atribuída!")
from src.auth.datastore import user_datastore
from src.auth.datastore import admin_datastore

def init_app(app):
    # a inicialização do Flask-Security já é feita no __init__.py principal
    # aqui podemos adicionar outras configurações específicas de auth se necessário
    pass

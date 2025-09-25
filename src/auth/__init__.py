from ..extensions import Security
from .datastore import user_datastore

def init_auth(app):
    Security(app, user_datastore)
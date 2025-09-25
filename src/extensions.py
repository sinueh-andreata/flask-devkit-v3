from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

db = SQLAlchemy()

csrf = CSRFProtect()

security = Security()

limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
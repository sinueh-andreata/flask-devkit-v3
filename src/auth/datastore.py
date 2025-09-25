from flask_security import SQLAlchemyUserDatastore
from ..extensions import db
from ..models.models import User, Role, Admin

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
admin_datastore = SQLAlchemyUserDatastore(db, Admin, Role)
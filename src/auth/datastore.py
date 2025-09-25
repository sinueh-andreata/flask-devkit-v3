from flask_security import SQLAlchemyUserDatastore
from ..extensions import db
from ..models.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
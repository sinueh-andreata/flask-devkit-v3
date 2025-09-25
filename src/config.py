import os
from dotenv import load_dotenv

load_dotenv()

#importando variaveis do .env e definindo configurações base
class ConfigBase:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True
    
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_EMAIL_SENDER = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False


# Configurações específicas para desenvolvimento 
class ConfigDev(ConfigBase):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

# Configurações específicas para produção
class ConfigProd(ConfigBase):
    DEBUG = False

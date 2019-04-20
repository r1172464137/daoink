class Config(object):
    SECRET_KEY = ''

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://YOUR_DATABASE_USERNAME:YOURPASSWORD@YOUR_DATABASE_IP:3306/YOUR_DATABASE_NAME"

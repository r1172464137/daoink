class Config(object):
    SECRET_KEY = '7a71ea10c4af9f16f020488e115b32fd'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://daoink:daoinkdream2020@60.205.176.255:3306/rooprint"

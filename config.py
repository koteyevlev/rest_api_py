class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://entrant:@localhost/rest_api1'
    SECRET_KEY = 'something very secret'
    PORT = int("8080")

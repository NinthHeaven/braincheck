# importing configurations
import os

# default configs for local
class defaultConfig(object):
    DEBUG = False
    SECRET_KEY = 'YK\xa0f\n\x82r\x96\xe4\xb2f\x7f\n\xab\x1d\x9bj\xf4\xf1U\x91\xaa\x04\xb2'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# developer configs
class devConfig(defaultConfig):
    DEBUG = True

 # configs for heroku app (identical to default atm)   
class publicConfig(defaultConfig):
    DEBUG = False
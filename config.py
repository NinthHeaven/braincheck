# importing configurations
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# default configs for local
class defaultConfig(object):
    DEBUG = False
    SECRET_KEY = 'YK\xa0f\n\x82r\x96\xe4\xb2f\x7f\n\xab\x1d\x9bj\xf4\xf1U\x91\xaa\x04\xb2'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'users.db')
    #if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        #SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['brainboterrors@gmail.com']
    MAX_CONTENT_LENGTH = 1024 * 1024


# developer configs
class devConfig(defaultConfig):
    DEBUG = True

 # configs for heroku app (identical to default atm)   
class publicConfig(defaultConfig):
    DEBUG = False
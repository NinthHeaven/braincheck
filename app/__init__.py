from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from config import defaultConfig
from flask_bootstrap import Bootstrap

#os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
# FOR IMAGE TESTING
TEST_PHOTOS = os.path.join('static', 'uploads')
#print(TEST_PHOTOS)

app = Flask(__name__)

# App configurations
app.config.from_object(defaultConfig)
app.config['UPLOAD_FOLDER'] = TEST_PHOTOS

# sqlalchemy object
db = SQLAlchemy(app)

# For migrating mods of db to another place 
migrate = Migrate(app, db)

# Manages login state and allows remember me function to work
login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

# Ensures email logger runs during production
# DOES NOT WORK AS INTENDED, FIX LATER (bug) --fixed--
if not app.debug:
   if app.config['MAIL_SERVER']:
      auth = None
      if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
         auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
      secure = None
      if app.config['MAIL_USE_TLS']:
         secure = ()
      mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                 fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                                 toaddrs=app.config['ADMINS'], subject='Braincheck Failure',
                                 credentials=auth, secure=secure)
      mail_handler.setLevel(logging.ERROR)
      app.logger.addHandler(mail_handler)

   # Creates logs
   if not os.path.exists('logs'):
      os.mkdir('logs')
   file_handler = RotatingFileHandler('logs/braincheck.log', maxBytes=10287, backupCount=10)
   file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
   file_handler.setLevel(logging.INFO)
   app.logger.addHandler(file_handler)
   app.logger.info('Braincheck Startup Info')



# import model
from app import models, routes, errors

# basic starting 
#if __name__ == "__main__":
   # app.run()
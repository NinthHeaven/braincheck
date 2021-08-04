from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class Usernames(db.Model, UserMixin):

    # Keep same name of dataframe
    __tablename__ = "users"

    # Setting columns of the usernames dataframe using SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    pass_hash = db.Column(db.String)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Users can create comments. CHANGE THIS LATER TO REQUESTS/EDITS!!!!!
    comments = db.relationship('Comments', backref='author', lazy='dynamic')

    # Users can rate images
    ratings = db.relationship('Ratings', backref='rater', lazy='dynamic')

    # Admin and Bot can broadcast message
    broadcasts = db.relationship('Broadcasts', backref='mod', lazy='dynamic')

    # Hash password for better security
    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.pass_hash, password)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


    #def __init__(self, username):
        #self.username = username

    def __repr__(self):
        return '<username: {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return Usernames.query.get(int(id))


class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Notice how the table name is used here instead of the model name
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #def __init__(self, body, author):
        #self.body = body
        #self.author = author

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Ratings(db.Model):

    __tablename__ = 'pic_ratings'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Rating {}>'.format(self.rating)

class Broadcasts(db.Model):

    __tablename__ = 'broadcasts'

    id = db.Column(db.Integer, primary_key=True)
    broadcast = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
from app import db

class Usernames(db.Model):

    # Keep same name of dataframe
    __tablename__ = "users"

    # Setting columns of the usernames dataframe using SQLAlchemy
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '\nusername: {} \n password: {}'.format(self.username, self.password)
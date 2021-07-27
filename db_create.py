from app import db
from models import Usernames

# Create database and tables
db.create_all()

# add data
db.session.add(Usernames('admin', 'admin'))
db.session.add(Usernames('test', 'test'))

# commit changes
db.session.commit()
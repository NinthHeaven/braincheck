from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
#import sqlite3

app = Flask(__name__)

# For login sessions and privacy, but make it more random later
app.secret_key = "this is a key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy object
db = SQLAlchemy(app)

# import model
from models import Usernames

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Sorry, you can't view this page without logging in.")
            return redirect(url_for('login'))
    return wrap

@app.route("/")
@login_required
def home_page():
    users = []
    try:
        # Create a temporary database connection
        users = db.session.query(Usernames).all()
    except sqlite3.OperationalError:
        flash("No users are registered at the moment.")
    return render_template('home.html')

@app.route("/greet/")
def greet():
    return render_template('site.html')

# Creating login page
# Once this works, make sure that users see login page before anything else (add logic later)
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Creating the error message
    error = None
    # Only allowing people who put admin as both user/pass to access website
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Sorry, unless you put the right info you can\'t login.'
        else:
            session['logged_in'] = True
            flash("Welcome! Redirecting you now...")
            return redirect(url_for('home_page'))

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("Goodbye, we will miss you!")
    return redirect(url_for('home_page'))

#def connect_to_db():
    #return sqlite3.connect(app.database)

# basic starting 
if __name__ == "__main__":
    app.run(debug=True)
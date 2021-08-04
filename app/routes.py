from flask import render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import ImgRating, Login, Register, EditProfile, Notifications, ImgUploader
from app.models import Usernames, Ratings, Broadcasts
from datetime import datetime
import os
# Constantly update the time a user accesses the page
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/")
@login_required
def home_page():
    # Create a temporary database connection
    users = db.session.query(Usernames).all()
    return render_template('home.html', users=users)

@app.route("/greet/")
def greet():
    return render_template('site.html')

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

# Creating login page
# Once this works, make sure that users see login page before anything else (add logic later)
@app.route("/login", methods=['GET', 'POST'])
def login():
    # If the user is already logged in, get them back to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = Login()
    # Creating the error message
    error = None
    # Check if username exists or if password matches
    if form.validate_on_submit():
        user = Usernames.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # Redirect user to page they wanted to access (might delete later)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_page')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = Register()
    if form.validate_on_submit():
        user = Usernames(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = Usernames.query.filter_by(username=username).first_or_404()
    announcements = db.session.query(Broadcasts).all()
    comments = [
        {'author': user, 'body': 'Hi there I am the admin'},
    ]
    ## for admin and bot access only...
    form = Notifications()
    if form.validate_on_submit():
        message = Broadcasts(broadcast=form.notif.data)
        db.session.add(message)
        db.session.commit()
        flash('Message has been sent to the site.')
        return redirect(url_for('user', username=current_user.username))   
    return render_template('user.html', user=user, comments=comments, announcements=announcements, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@app.route('/logs')
@login_required
def logs():
    full_pathname = os.path.join(app.config['UPLOAD_FOLDER'], 'cat-sample_1313.jpg')
    #cats = os.listdir('static/test_photos/')
    return render_template('logs.html')

@app.route('/image/<filename>')
@login_required
def image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/rater', methods=['GET', 'POST'])
@login_required
def rater():
    all_ratings = db.session.query(Ratings).all()
    form = ImgRating()
    if form.validate_on_submit():
        #current_user.rating = form.rating.data
        user = Usernames.query.filter_by(username=current_user.username).first_or_404()
        #ratings = [{'rater': user, 'rating': current_user.rating}]
        img_rating = Ratings(rating=form.rating.data, rater=user)
        db.session.add(img_rating)
        db.session.commit()
        flash('Your rating has been noted.')
        return redirect(url_for('rater'))
    return render_template('rater.html', form=form, all_ratings=all_ratings)

# This will eventually become the rater page, this is just for testing.
@app.route('/uploader', methods=['GET', 'POST'])
@login_required
def uploader():
    form = ImgUploader()
    files = os.listdir('static/uploads')
    if form.validate_on_submit():
        # Get uploaded file and check if it's an empty submission
        uploaded_img = secure_filename(form.image.data.filename)
        form.image.data.save(os.path.join('static/uploads', uploaded_img))
        return redirect(url_for('uploader'))
    return render_template('uploader.html', form=form, files=files)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Goodbye, we will miss you!")
    return redirect(url_for('home_page'))

#def connect_to_db():
    #return sqlite3.connect(app.database)
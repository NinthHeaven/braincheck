from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import Usernames

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField('Enter password again', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # Make sure username doesn't exist already
        user = Usernames.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists.')

class EditProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = Usernames.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('This username is already taken.')

class ImgRating(FlaskForm):
    #username = StringField('Username', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit Rating')

# MAKE THIS AVAILABLE TO ADMIN ONLY!!!!!
class Notifications(FlaskForm):
    notif = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Broadcast message')

class ImgUploader(FlaskForm):
    image = FileField('Image', validators=[FileRequired(),
                                           FileAllowed(['png', 'jpg'], "Please upload .png or .jpg files")])
    submit = SubmitField('Upload Image')

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from on_blog.models import User


class RegistrationForm(FlaskForm):
    # username validations - not empty amd length
    username = StringField('Username', validators=[DataRequired(), Length(max=30, min=5)])

    #email validators - not emplty and should follow email format
    email = StringField('Email', validators=[DataRequired(), Email()])

    #password validator - not empty
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username is taken. Please choose a different one")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one")


class LoginForm(FlaskForm):
    #email validators - not emplty and should follow email format
    email = StringField('Email', validators=[DataRequired(), Email()])

    #password validator - not empty
    password = PasswordField("Password", validators=[DataRequired()])

    remember = BooleanField("Remember me next time")
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    # username validations - not empty amd length
    username = StringField('Username', validators=[DataRequired(), Length(max=30, min=5)])

    #email validators - not emplty and should follow email format
    email = StringField('Email', validators=[DataRequired(), Email()])

    # image field validator
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username!= username.data:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different one")

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one")

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset ')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("No account with that email found")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')






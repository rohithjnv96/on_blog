from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

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
            raise ValidationError("That username is take. Please choose a different one")

    def validate_email(self, email):
        user = User.query.filter_by(username = email.data).first()
        if user:
            raise ValidationError("That email is take. Please choose a different one")


class LoginForm(FlaskForm):
    #email validators - not emplty and should follow email format
    email = StringField('Email', validators=[DataRequired(), Email()])

    #password validator - not empty
    password = PasswordField("Password", validators=[DataRequired()])

    remember = BooleanField("Remember me next time")
    submit = SubmitField('Log In')


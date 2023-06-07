from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    # username validations - not empty amd length
    username = StringField('Username', validators=[DataRequired(), Length(max=30, min=5)])

    #email validators - not emplty and should follow email format
    email = StringField('Email', validators=[DataRequired(), Email()])

    #password validator - not empty
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    #email validators - not emplty and should follow email format
    email = StringField('Email', validators=[DataRequired(), Email()])

    #password validator - not empty
    password = PasswordField("Password", validators=[DataRequired()])


    remember = BooleanField("Remember me next time")

    submit = SubmitField('Sign Up')


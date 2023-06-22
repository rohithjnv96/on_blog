from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

import logging

from on_blog import app, bcrypt, db
from on_blog.models import User, Post
from on_blog.forms import LoginForm, RegistrationForm

logging.basicConfig(level="DEBUG")

postz = [
    {
        'author': 'corey qedcsx',
        'title': 'blog post 1',
        'content': 'First post',
        'date_posted': 'april 13,1222'
    },
    {
        'author': 'corey qedcsx 2',
        'title': 'blog post 2',
        'content': 'Second post',
        'date_posted': 'april 16,1222'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", postz=postz, title="ebvhls")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # if user id already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        logging.debug("form validated")
        # success - is bootstrap part
        flash(f'You account has been created successfully, you are now able to login','success')
        return redirect(url_for('login'))
    logging.debug("form not validated")
    return render_template('register.html', title="Register", form=form)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if user id already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        logging.debug("form validated")

        # check if email exists in db
        user = User.query.filter_by(email = form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # logging in
            login_user(user = user, remember = form.remember.data)

            # login and returning to page requesting login
            request_from_page = request.args.get('next')
            logging.debug(f'request from page {request_from_page}')
            return redirect(request_from_page) if request_from_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful: please check email and password!', 'danger')
    logging.debug("form not validated")
    return render_template('login.html', title="Login", form=form)

@app.route("/logout" , methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account" , methods=['GET'])
@login_required
def account():
    return render_template('account.html', title="Account")


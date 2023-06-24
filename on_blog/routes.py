import os
import secrets

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

import logging

from on_blog import app, bcrypt, db
from on_blog.models import User, Post
from on_blog.forms import LoginForm, RegistrationForm, UpdateAccountForm

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

def save_picture_to_db(form_pic):
    name_hex = secrets.token_hex(8)
    # form.picture has data form.picture.data has filename
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_name = name_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_name)

    # resizing image
    output_size = (125,125)
    profile_pic = Image.open(form_pic)
    profile_pic.thumbnail(output_size)


    profile_pic.save(pic_path)
    return pic_name

def delete_picture(prev_image_name):
    pic_path = os.path.join(app.root_path, 'static/profile_pics')
    if os.path.exists(pic_path + '/' + prev_image_name):
        # file exists, delete it
        os.remove(pic_path + '/' + prev_image_name)
        return "file removed"
    return "file was not removed"



@app.route("/account" , methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        logging.debug("form validated")
        # updating user details
        if form.picture.data is not None:
            prev_image_name = current_user.image_file
            logging.debug(f"picture exists: {prev_image_name}")
            pic_name = save_picture_to_db(form.picture.data)
            current_user.image_file = pic_name
            if prev_image_name != 'default.jpeg':
                inf = delete_picture(prev_image_name)
                logging.debug(f'prev image del')
        current_user.username = form.username.data
        current_user.email = form.email.data
        logging.debug("user data about to be updated")
        db.session.commit()
        flash("Your profile was updated successfully!!!", category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    user_image = url_for('static', filename = 'profile_pics/'+ current_user.image_file)
    return render_template('account.html', title="Account", image_file = user_image, form = form)


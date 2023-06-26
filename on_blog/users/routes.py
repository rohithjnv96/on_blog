import logging

from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

from on_blog import bcrypt, db
from on_blog.models import User, Post
from on_blog.users.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm, UpdateAccountForm
from on_blog.users.utils import send_reset_email, save_picture_to_db, delete_picture

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # if user id already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        # success - is bootstrap part
        flash(f'You account has been created successfully, you are now able to login','success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)

@users.route("/login" , methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if user id already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():

        # check if email exists in db
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # logging in
            login_user(user = user, remember = form.remember.data)

            # login and returning to page requesting login
            request_from_page = request.args.get('next')
            return redirect(request_from_page) if request_from_page else redirect(url_for('main.home'))
        else:
            flash(f'Login unsuccessful: please check email and password!', 'danger')
    return render_template('login.html', title="Login", form=form)

@users.route("/logout" , methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account" , methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # updating user details
        logging.debug('form pic data: {form.picture.data}')
        if form.picture.data:
            prev_image_name = current_user.image_file
            pic_name = save_picture_to_db(form.picture.data)
            current_user.image_file = pic_name
            if prev_image_name != 'default.jpeg':
                info = delete_picture(prev_image_name)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your profile was updated successfully!!!", category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    user_image = url_for('static', filename = 'profile_pics/'+ current_user.image_file)
    return render_template('account.html', title="Account", image_file = user_image, form = form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset the password', category='info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', form = form, title='Reset Password')

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def token_verify(token):
    if current_user.is_authenticated:
        redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Recieved either invalid or expired token", category='warning')
        return redirect(url_for('users.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pw
        db.session.commit()
        flash('You password has been updated successfully','success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
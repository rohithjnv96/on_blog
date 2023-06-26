import os
import secrets

from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from PIL import Image

import logging

from itsdangerous import TimedSerializer

from on_blog import app, bcrypt, db, mail
from on_blog.models import User, Post
from on_blog.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, ResetPasswordForm, RequestResetForm

logging.basicConfig(level="DEBUG")

@app.route("/")
@app.route("/home")
def home():
    page_no = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.time.desc()).paginate(per_page=5, page=page_no)
    return render_template("home.html", posts=posts, title="Home Page")

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

@app.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    # id, title, time, content, user_id
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", category="success")
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post", form = form, legend='Create Post ')


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    elif form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updates', category='success')
        return redirect(url_for('post', post_id= post.id))
    return render_template('create_post.html', title="Update Post", form = form)


@app.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        db.session.delete(post)
        db.session.commit()
        flash("This post has been deleted successfully", category='success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page_no = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.time.desc()).paginate(per_page=5, page=page_no)
    return render_template("user_posts.html", posts=posts, title="User Posts", user=user)

def send_reset_email(user):
    token = User.get_reset_token(user)
    ext_url = str(url_for("token_verify", token=token, _external=True))

    msg = Message(
        subject='Password reset request for on-blog account',
        sender=('on-Blog website', 'no-reply-on_blog@gmail.com'),
        recipients=[user.email])
    msg.body = '''To reset password visit the following link: {}\nIf you did not make this request, please ignore the message.'''.format(ext_url)
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset the password', category='info')
        return redirect(url_for('login'))
    return render_template('request_reset.html', form = form, title='Reset Password')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def token_verify(token):
    if current_user.is_authenticated:
        redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Recieved either invalid or expired token", category='warning')
        return redirect(url_for('reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pw
        db.session.commit()
        flash('You password has been updated successfully','success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)






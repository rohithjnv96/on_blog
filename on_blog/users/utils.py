import os
import secrets

from PIL import Image
from flask import url_for
from flask_mail import Message
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

from on_blog import mail
from on_blog.models import User


def save_picture_to_db(form_pic):
    name_hex = secrets.token_hex(8)
    # form.picture has data form.picture.data has filename
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_name = name_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_name)

    # resizing image
    output_size = (350,350)
    profile_pic = Image.open(form_pic)
    profile_pic.thumbnail(output_size)


    profile_pic.save(pic_path)
    return pic_name

def send_reset_email(user):
    token = User.get_reset_token(user)
    ext_url = str(url_for("users.token_verify", token=token, _external=True))
    msg = Message(
        subject='Password reset request for on-blog account',
        sender=('on-Blog website', 'no-reply-on_blog@gmail.com'),
        recipients=[user.email])
    msg.body = '''To reset password visit the following link: {}\nIf you did not make this request, please ignore the message.'''.format(ext_url)
    mail.send(msg)


def send_verification_email(username, email, token):
    message = Message(
        subject = "Welcome to on_blog! Verify Your Email",
        sender = ('on-Blog website', 'no-reply-on_blog@gmail.com'),
        recipients = [str(email)],
        body = f'''Hello {username},

Thank you for registering with on_blog! To complete your registration and verify your email address, please click the following link:

{token}

If you did not sign up for on_blog, please ignore this email.

Note: This link will expire in 5 minuted for security purposes. If the link has expired, please visit our website and request a new verification email.

Thank you,
The on_blog Team''')
    mail.send(message)
    return None


def delete_picture(prev_image_name):
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics')
    if os.path.exists(pic_path + '/' + prev_image_name):
        # file exists, delete it
        os.remove(pic_path + '/' + prev_image_name)
        return "file removed"
    return "file was not removed"

def get_timed_serialized_token(payload):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(payload)
    return token

def get_data_from_timed_serialized_token(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    data = s.loads(token, max_age=300)
    return data


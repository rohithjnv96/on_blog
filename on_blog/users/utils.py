import os
import secrets

from PIL import Image
from flask import url_for
from flask_mail import Message

from on_blog import mail, app
from on_blog.models import User


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

def send_reset_email(user):
    token = User.get_reset_token(user)
    ext_url = str(url_for("users.token_verify", token=token, _external=True))
    msg = Message(
        subject='Password reset request for on-blog account',
        sender=('on-Blog website', 'no-reply-on_blog@gmail.com'),
        recipients=[user.email])
    msg.body = '''To reset password visit the following link: {}\nIf you did not make this request, please ignore the message.'''.format(ext_url)
    mail.send(msg)


def delete_picture(prev_image_name):
    pic_path = os.path.join(app.root_path, 'static/profile_pics')
    if os.path.exists(pic_path + '/' + prev_image_name):
        # file exists, delete it
        os.remove(pic_path + '/' + prev_image_name)
        return "file removed"
    return "file was not removed"

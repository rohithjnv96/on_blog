from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from on_blog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    page_no = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.time.desc()).paginate(per_page=5, page=page_no)
    return render_template("home.html", posts=posts, title="Home Page")

@main.route("/welcome")
def welcome():
    if current_user.is_authenticated:
        flash('User already logged in !!!', 'info')
        return redirect(url_for('main.home'))
    return render_template("welcome.html", title="Welcome Page")


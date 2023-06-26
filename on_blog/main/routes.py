from flask import Blueprint, request, render_template
from on_blog.models import Post
from on_blog import templates

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page_no = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.time.desc()).paginate(per_page=5, page=page_no)
    return render_template("home.html", posts=posts, title="Home Page")

@main.route("/about")
def about():
    return render_template("about.html")
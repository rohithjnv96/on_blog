from flask import Blueprint, render_template, abort, request, redirect, flash, url_for
from flask_login import login_required, current_user

from on_blog import db
from on_blog.models import Post, User
from on_blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@posts.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
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
        return redirect( url_for('posts.post', post_id= post.id))
    return render_template('create_post.html', title="Update Post", form = form)


@posts.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        db.session.delete(post)
        db.session.commit()
        flash("This post has been deleted successfully", category='success')
    return redirect(url_for('main.home'))


@posts.route('/post/new', methods=['POST', 'GET'])
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
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title="New Post", form = form, legend='Create Post ')

@posts.route("/user/<string:username>")
@login_required
def user_posts(username):
    page_no = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.time.desc()).paginate(per_page=5, page=page_no)
    return render_template("user_posts.html", posts=posts, title="User Posts", user=user)
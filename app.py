from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from forms import RegistrationForm, LoginForm
import logging

logging.basicConfig(level="DEBUG")

app = Flask(__name__)
app.config['SECRET_KEY'] = '79d0f69fc13be5944aab2a4e096f501c4a70a426f15c661f0467d276c255d3ff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # hashing takes 20 chars
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    # hashing takes 60 chars
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship("Post", backref = "author", lazy = True)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image_file}")'

class Post(db.Model):
    id = db.Column(db.Integer, primary=True)
    title = db.Column(db.String(100), nullable=False)
    # no () for utcnow cause we are sending it as a variable
    title = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.COlumn(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


    def __repr__(self):
        return f'Post("{self.title}", "{self.title}"'






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
    if form.validate_on_submit():
        logging.debug("form validated")
        # success - is bootstrap part
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    logging.debug("form not validated")
    return render_template('register.html', title="Register", form=form)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        logging.debug("form validated")
        if form.email.data == "admin@blog.com" and form.password.data == "admin123":
            flash(f'Successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful: please check username and password!', 'danger')
    logging.debug("form not validated")
    return render_template('login.html', title="Login", form=form)



if __name__ == "__main__":
    app.run(debug=True)



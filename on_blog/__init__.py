from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

# mail config
app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('APP_EMAIL')
# password is app password generated in the google settings
app.config['MAIL_PASSWORD'] = os.environ.get('APP_PASSWORD')
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# to prettify "please-login" message thrown by login manager
login_manager.login_message_category = "danger"

# create all tables
from on_blog import models
with app.app_context():
    db.create_all()

from on_blog.main.routes import main
from on_blog.posts.routes import posts
from on_blog.users.routes import users
app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(users)



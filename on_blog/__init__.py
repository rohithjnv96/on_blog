from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '79d0f69fc13be5944aab2a4e096f501c4a70a426f15c661f0467d276c255d3ff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# create all tables
from on_blog import models
with app.app_context():
    db.create_all()

from on_blog import routes
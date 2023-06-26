from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# initializing db
db = SQLAlchemy()

# password hashing service
bcrypt = Bcrypt()

# flask-loging configs
login_manager = LoginManager()
login_manager.login_view = 'users.login'
# to prettify "please-login" message thrown by login manager
login_manager.login_message_category = "danger"

#flask-mail config
mail = Mail()

# creating  app instance
from on_blog.config import Config
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # binding extensions to the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # create/loading all tables for db
    from on_blog import models
    with app.app_context():
        db.create_all()


    # adding all blueprints in the project
    from on_blog.main.routes import main
    from on_blog.posts.routes import posts
    from on_blog.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app






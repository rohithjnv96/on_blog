import os

class Config:
    # configuration for flask app
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_PATH')

    # configuration for mailing service(password is app password generated in google settings)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME = os.environ.get('APP_EMAIL')
    MAIL_PASSWORD = os.environ.get('APP_PASSWORD')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
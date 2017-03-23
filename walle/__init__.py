from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.login import LoginManager
from walle.deploy.deploy import deploy
from walle.user.user import user_blue_print
from walle.user.passport import passport_blue_print
from walle.common import models
from flask_mail import Mail
from flask_login import LoginManager
from walle.common import models


VERSION = (0, 2)

__version__ = ".".join(map(str, VERSION))
__status__ = "Alpha"
__description__ = "Simple blog system powered by Flask"
__author__ = "defshine"
__email__ = "crazyxin1988@gmail.com"
__license__ = "MIT License"

app = Flask(__name__)
app.config.from_object('walle.config.default.DefaultConfig')
app.secret_key = 'xxxxyyyyyzzzzz'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

def create_app():
    register_database(app)
    register_blueprint(app)
    # register_mail(app)
    # init_login(app)
    # create_admin(app, db)
    return app

#
# def register_log():
#     import logging
#     logging.basicConfig()
#     logging.getLogger().setLevel(logging.DEBUG)
#
#
def register_database(app):
    models.db.init_app(app)
    models.db.app = app


def register_mail(app):
    mail = Mail(app)

def register_blueprint(app):
    app.register_blueprint(deploy, url_prefix='/deploy')
    app.register_blueprint(user_blue_print, url_prefix='/user')
    app.register_blueprint(passport_blue_print, url_prefix='/passport')

#
#
# # Initialize flask-login
# def init_login(app):
#     login_manager = LoginManager()
#     login_manager.init_app(app)
#
#     # Create user loader function
#     @login_manager.user_loader
#     def load_user(user_id):
#         from app.core.models import User
#         return db.session.query(User).get(user_id)




@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=int(user_id)).first()

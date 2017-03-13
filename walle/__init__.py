from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.login import LoginManager
from walle.deploy.deploy import deploy
from walle.common import models


VERSION = (0, 2)

__version__ = ".".join(map(str, VERSION))
__status__ = "Alpha"
__description__ = "Simple blog system powered by Flask"
__author__ = "defshine"
__email__ = "crazyxin1988@gmail.com"
__license__ = "MIT License"


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_database(app)
    register_blueprint(app)
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


def register_blueprint(app):
    app.register_blueprint(deploy, url_prefix='/deploy')

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





# project/server/__init__.py


#############
#  imports  #
#############

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


############
#  config  #
############

app = Flask(__name__)


if 'APP_SETTINGS' in os.environ:
    app_settings = os.environ['APP_SETTINGS']
else:
    app_settings = 'project.server.config.DevelopmentConfig'

app.config.from_object(app_settings)


################
#  extensions  #
################

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

from project.server.models import User


################
#  blueprints  #
################

from project.server.user.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/auth')


#################
#  flask-login  #
#################

from project.server.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


############
#  routes  #
############

@app.route("/")
def hello():
    return "Hello World!"

# project/server/__init__.py


#############
#  imports  #
#############

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap


############
#  config  #
############

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)


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
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from project.server.models import User


################
#  blueprints  #
################

from project.server.user.views import user_blueprint
from project.server.bathroom.views import bathroom_blueprint
from project.server.main.views import main_blueprint

app.register_blueprint(user_blueprint, url_prefix='/auth')
app.register_blueprint(bathroom_blueprint, url_prefix='/bathrooms')
app.register_blueprint(main_blueprint, url_prefix='/')


#################
#  flask-login  #
#################

from project.server.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

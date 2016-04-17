# project/server/__init__.py


#############
#  imports  #
#############

import os
from flask import Flask


############
#  config  #
############

app = Flask(__name__)


if 'APP_SETTINGS' in os.environ:
    app_settings = os.environ['APP_SETTINGS']
else:
    app_settings = 'project.server.config.DevelopmentConfig'

app.config.from_object(app_settings)


############
#  routes  #
############

@app.route("/")
def hello():
    return "Hello World!"

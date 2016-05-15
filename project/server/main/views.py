# project/server/main/views.py


#############
#  imports  #
#############

from flask import Blueprint, render_template

from project.server.models import Bathroom


############
#  config  #
############

main_blueprint = Blueprint('main', __name__,)


############
#  routes  #
############

@main_blueprint.route("/")
def index():
    return render_template(
        'main/index.html',
        bathrooms=Bathroom.query.all()
    )

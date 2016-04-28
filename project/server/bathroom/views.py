# project/server/bathroom/views.py


#############
#  imports  #
#############

from flask import Blueprint


############
#  config  #
############

bathroom_blueprint = Blueprint('bathroom', __name__,)


############
#  routes  #
############

@bathroom_blueprint.route('/<id>')
def bathroom(id):
    return id

# project/server/bathroom/views.py


#############
#  imports  #
#############

import json
from flask import Blueprint, Response

from project.server.models import Bathroom


############
#  config  #
############

bathroom_blueprint = Blueprint('bathroom', __name__,)


############
#  routes  #
############

@bathroom_blueprint.route('/')
def get_all_bathrooms():
    all_bathrooms = Bathroom.query.all()
    resp = Response(
        json.dumps(Bathroom.serialize_list(all_bathrooms)),
        mimetype='application/json'
    )
    return resp

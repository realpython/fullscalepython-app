# project/server/bathroom/views.py


#############
#  imports  #
#############

import json
from flask import Blueprint

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
    return json.dumps(Bathroom.serialize_list(all_bathrooms))

# project/server/bathroom/views.py


#############
#  imports  #
#############

import json
from flask import Blueprint, Response, request

from project.server import db
from project.server.models import Bathroom, Rating


############
#  config  #
############

bathroom_blueprint = Blueprint('bathroom', __name__,)


############
#  routes  #
############

@bathroom_blueprint.route('/', methods=['GET', 'POST'])
def get_all_bathrooms():
    if request.method == 'GET':
        all_bathrooms = Bathroom.query.all()
        resp = Response(
            json.dumps(Bathroom.serialize_list(all_bathrooms)),
            mimetype='application/json'
        )
        return resp
    elif request.method == 'POST':
        data = request.get_json()
        bathroom = Bathroom.query.filter_by(name=data['name']).first()
        bathroom.id
        new_rating = Rating(
            bathroom_id=bathroom.id,
            rating=data['rating']
        )
        db.session.add(new_rating)
        db.session.commit()
        return json.dumps({'status': 'success'})

# project/server/bathroom/views.py


#############
#  imports  #
#############

import math
import json
from flask import Blueprint, Response, request
from flask.ext.login import current_user

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
        if not current_user.is_authenticated:  # fail fast!
            response = json.dumps({
                'status': 'error',
                'message': 'You must be logged in to rate.'
            })
            return response, 401
        else:
            data = request.get_json()
            bathroom = Bathroom.query.filter_by(name=data['name']).first()
            bathroom.id
            new_rating = Rating(
                user_id=current_user.id,
                bathroom_id=bathroom.id,
                rating=data['rating']
            )
            db.session.add(new_rating)
            db.session.commit()
            ratings = Rating.query.all()
            bathroom.rating = 0
            bathroom.rating_count = 0
            bathroom.rating_total = 0
            for rating in ratings:
                if bathroom.id == rating.bathroom_id:
                    bathroom.rating_total += rating.rating
                    bathroom.rating_count += 1
            bathroom.rating = math.ceil(bathroom.rating_total / bathroom.rating_count)
            data = {
                'name': bathroom.name,
                'rating': bathroom.rating,
                'count': bathroom.rating_count
            }
            return json.dumps({
                'status': 'success',
                'message': 'Thank you. Rating sucessfully recorded.',
                'data': data
            })

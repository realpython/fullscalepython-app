# project/server/main/views.py


#############
#  imports  #
#############

import math
from flask import Blueprint, render_template

from project.server.models import Bathroom, Rating


############
#  config  #
############

main_blueprint = Blueprint('main', __name__,)


############
#  routes  #
############

@main_blueprint.route("/")
def index():
    bathrooms = Bathroom.query.all()
    ratings = Rating.query.all()
    for bathroom in bathrooms:
        bathroom.rating = 0
        bathroom.rating_count = 0
        bathroom.rating_total = 0
        for rating in ratings:
            if bathroom.id == rating.bathroom_id:
                bathroom.rating_total += rating.rating
                bathroom.rating_count += 1
        bathroom.rating = math.ceil(bathroom.rating_total / bathroom.rating_count)
    return render_template(
        'main/index.html',
        bathrooms=bathrooms
    )

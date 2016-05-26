# project/server/main/views.py


#############
#  imports  #
#############

from flask import Blueprint, render_template

from project.server.models import Bathroom, Ratings


############
#  config  #
############

main_blueprint = Blueprint('main', __name__,)


############
#  routes  #
############

@main_blueprint.route("/")
def index():
    all_ratings = Ratings.query.all()
    all_bathrooms = Bathroom.query.all()
    updated_bathrooms = []
    for bathroom in all_bathrooms:
        bathroom.rating = 0
        for rating in all_ratings:
            if bathroom.id == rating.bathroom_id:
                if rating.rating is not None:
                    bathroom.rating += rating.rating
        updated_bathrooms.append(bathroom)
    return render_template(
        'main/index.html',
        bathrooms=updated_bathrooms
    )

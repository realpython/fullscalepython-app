# project/server/models.py


import datetime
from sqlalchemy.inspection import inspect
from sqlalchemy.dialects.postgresql import JSON

from project.server import app, db, bcrypt


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Binary(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        )
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Bathroom(db.Model, Serializer):

    __tablename__ = 'bathrooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    open_year_round = db.Column(db.Boolean, nullable=False)
    handicap_accessible = db.Column(db.Boolean, nullable=False)
    borough = db.Column(db.String(255), nullable=False)
    latlong = db.Column(JSON, nullable=False)

    def __init__(self, name, location, open_year_round, handicap_accessible, borough, latlong):
        self.name = name
        self.location = location
        self.open_year_round = open_year_round
        self.handicap_accessible = handicap_accessible
        self.borough = borough
        self.latlong = latlong

    def __repr__(self):
        return '<Bathroom {0}>'.format(self.name)


class Ratings(db.Model):

    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathrooms.id'))
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, rating):
        self.rating = rating

    def __repr__(self):
        return '<Rating {0}>'.format(self.rating)

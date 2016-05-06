# manage.py


import unittest
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from project.server import app, db
from project.server.models import Bathroom


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def seed():
    """Seeds the db."""
    # from pprint import pprint
    import requests
    import json

    new_data = []
    URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_geodata(address):
        payload = {'address': address}
        response = requests.get(URL, params=payload)
        return response.json()

    with open('bathrooms.json') as file:
        data = json.load(file)
        with open('bathrooms2.json', 'w') as outfile:
            for line in data:
                updated_data = {}
                if hasattr(line, 'handicap_accessible'):
                    handicap = line['handicap_accessible']
                else:
                    handicap = 'No'
                try:
                    geodata = get_geodata(line['location'])
                    updated_data = {
                        'borough': line['borough'],
                        'location': line['location'],
                        'name': line['name'],
                        'open_year_round': line['open_year_round'],
                        'handicap_accessible': handicap,
                        'latlong': geodata["results"][0]["geometry"]["location"]
                    }
                    new_data.append(updated_data)
                except:
                    pass
            json.dump(new_data, outfile)


if __name__ == "__main__":
    manager.run()

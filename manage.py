# manage.py


import csv
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
    with open('bathrooms.csv', 'rt') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row[2] == 'Yes':
                openBoolean = True
            else:
                openBoolean = False
            if row[3] == 'Yes':
                handicapBoolean = True
            else:
                handicapBoolean = False
            if row[4] == 'Manhattan':
                db.session.add(Bathroom(
                    name=row[0],
                    location=row[1],
                    open_year_round=openBoolean,
                    handicap_accessible=handicapBoolean,
                    borough=row[4],
                    latlong=row[5],
                    rating=0,
                    rating_count=0
                ))
    db.session.commit()


if __name__ == "__main__":
    manager.run()

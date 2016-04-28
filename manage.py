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
    db.session.add(Bathroom(name='Gold Room'))
    db.session.commit()


if __name__ == "__main__":
    manager.run()

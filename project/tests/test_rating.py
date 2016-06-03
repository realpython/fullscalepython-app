# project/server/tests/test_rating.py


import unittest
from sqlalchemy.exc import IntegrityError

from base import BaseTestCase
from project.server import db
from project.server.models import Rating, User


class TestRatingModel(BaseTestCase):

    def test_valid_rating(self):
        # Ensure Rating model behaves correctly with valid data.
        user = User.query.first()
        query = Rating.query.filter_by(user_id=user.id).first()
        self.assertEqual(query.rating, 5)

    def test_invalid_rating(self):
        # Ensure Rating model behaves correctly with invalid data.
        rating = Rating(
            user_id=22,
            bathroom_id=999,
            rating=3
        )
        db.session.add(rating)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        with self.assertRaises(TypeError):
            rating = Rating(
                bathroom_id=999,
                rating=3
            )
        with self.assertRaises(TypeError):
            rating = Rating(
                user_id=22,
                rating=3
            )
            db.session.add(rating)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()

# project/server/tests/test_bathroom.py


import unittest


from base import BaseTestCase


class TestBathroomBlueprint(BaseTestCase):

    def test_user_registration(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.get('/bathrooms', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'application/json')
            self.assertIn(b'[{"location": "NYC", "name": "test bathroom", "id": 1}]', response.data)


if __name__ == '__main__':
    unittest.main()

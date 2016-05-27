# project/server/tests/test_main.py


import unittest

from base import BaseTestCase


class TestMainBlueprint(BaseTestCase):

    def test_index(self):
        # Ensure Flask is setup.
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Map', response.data)
        self.assertIn(b'<h2>Bathrooms</h2>', response.data)
        self.assertIn(b'<li data-address="NYC" data-rating="0">test bathroom</li>', response.data)


if __name__ == '__main__':
    unittest.main()

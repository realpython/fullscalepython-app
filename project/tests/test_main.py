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
        self.assertIn(b'<td id="bathroom-name" data-location="NYC" class="bathroom-name">test bathroom</td>', response.data)
        self.assertIn(b'<td id="bathroom-rating" class="bathroom-star-rating">', response.data)
        self.assertIn(b'<input id="star-input" value="5" data-step=1 data-size="xs" data-show-clear="false" data-show-caption="false" class="rating rating-loading">', response.data)
        self.assertIn(b'<td id="bathroom-rating-count"><span id="rating-count">1</span> total ratings</td>', response.data)


if __name__ == '__main__':
    unittest.main()

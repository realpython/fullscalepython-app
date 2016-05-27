# project/server/tests/test_bathroom.py


import json
import unittest

from base import BaseTestCase


class TestBathroomBlueprint(BaseTestCase):

    def test_bathroom_api_endpoint(self):
        # Ensure bathroom API behaves correctly.
        with self.client:
            response = self.client.get('/bathrooms', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'application/json')
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(data[0]['borough'], 'Manhattan')
            self.assertEqual(data[0]['handicap_accessible'], True)
            self.assertEqual(data[0]['open_year_round'], True)
            self.assertEqual(data[0]['latlong'], "{'lng': -73.9712488, 'lat': 40.7830603}")
            self.assertEqual(data[0]['rating'], 0)
            self.assertEqual(data[0]['rating_count'], 0)


if __name__ == '__main__':
    unittest.main()

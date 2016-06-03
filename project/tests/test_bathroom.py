# project/server/tests/test_bathroom.py


import json
import unittest

from base import BaseTestCase


class TestBathroomBlueprint(BaseTestCase):

    def test_bathroom_api_get_endpoint(self):
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

    def test_bathroom_api_post_endpoint_unauthenticated(self):
        # Ensure bathroom API behaves correctly when unauthenticated.
        with self.client:
            response = self.client.post(
                '/bathrooms/',
                data=json.dumps(dict(
                    name='test bathroom',
                    rating=2
                )),
                content_type='application/json',
                follow_redirects=True)
            self.assertEqual(response.status_code, 401)

    def test_bathroom_api_post_endpoint_authenticated(self):
        # Ensure bathroom API behaves correctly when authenticated.
        with self.client:
            self.client.post(
                '/auth/login',
                data=dict(email='ad@min.com', password='admin_user'),
                follow_redirects=True
            )
            response = self.client.post(
                '/bathrooms/',
                data=json.dumps(dict(
                    name='test bathroom',
                    rating=2
                )),
                content_type='application/json',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(
                data['message'],
                'Thank you. Rating sucessfully recorded.'
            )
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data'], {'name': 'test bathroom', 'rating': 4, 'count': 2})


if __name__ == '__main__':
    unittest.main()

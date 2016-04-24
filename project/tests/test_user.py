# project/server/tests/test_user.py


import unittest

from flask.ext.login import current_user

from base import BaseTestCase


class TestUserBlueprint(BaseTestCase):

    def test_register_route(self):
        # Ensure about route behaves correctly.
        response = self.client.get(
            '/auth/register',
            follow_redirects=True
        )
        self.assertIn(b'<h1>Please Register</h1>\n', response.data)

    def test_user_registration(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=dict(
                    email="test@tester.com",
                    username="testing",
                    password="testing",
                    confirm="testing"
                ),
                follow_redirects=True
            )
            self.assertIn(b'Thank you for registering.\n', response.data)
            self.assertTrue(current_user.email == "test@tester.com")
            self.assertTrue(current_user.is_active())
            self.assertEqual(response.status_code, 200)

    def test_user_registration_duplicate_username(self):
        # Ensure registration fails when a duplicate username is used.
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=dict(
                    email="new@email.com",
                    username="duplicate_user",
                    password="testing",
                    confirm="testing"
                ),
                follow_redirects=True
            )
            self.assertIn(b'Username must be unique.\n', response.data)
            self.assertEqual(response.status_code, 200)

    def test_user_registration_duplicate_email(self):
        # Ensure registration fails when a duplicate email is used.
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=dict(
                    email="duplcate@user.com",
                    username="new_user_name",
                    password="testing",
                    confirm="testing"
                ),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

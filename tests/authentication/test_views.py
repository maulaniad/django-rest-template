from decouple import config
from os.path import dirname, join

from rest_framework.test import APITestCase, APIClient

from tests.authentication.endpoints import AuthenticationEndpoints


CURRENT_DIR = dirname(__file__)

class TestAuthenticationViews(APITestCase):
    fixtures = [
        join(CURRENT_DIR, "fixtures/user.json"),
        join(CURRENT_DIR, "fixtures/profile.json"),
    ]

    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoints = AuthenticationEndpoints()
        self.user_data = {
            'username': config("TEST_USERNAME", default=None),
            'password': config("TEST_PASSWORD", default=None),
        }

    def tearDown(self) -> None:
        return super().tearDown()

    def test_login_success_with_valid_credentials(self):
        response = self.client.post(
            path=self.endpoints.login,
            data=self.user_data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_login_failure_with_invalid_username(self):
        response = self.client.post(
            path=self.endpoints.login,
            data={
                'username': "purposedly_invalid_username",
                'password': self.user_data['password'],
            },
            format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_login_failure_with_invalid_password(self):
        response = self.client.post(
            path=self.endpoints.login,
            data={
                'username': self.user_data['username'],
                'password': "purposedly_invalid_password",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_refresh_token(self):
        response = self.client.post(
            path=self.endpoints.login,
            data=self.user_data,
            format="json"
        )
        original_token = response.data['data']['token']

        response = self.client.get(
            path=self.endpoints.refresh_token,
            HTTP_AUTHORIZATION=f"Bearer {original_token}",
            format="json"
        )
        refreshed_token = response.data['data']['token']

        self.assertNotEqual(original_token, refreshed_token)

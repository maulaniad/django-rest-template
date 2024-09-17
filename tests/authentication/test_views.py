from decouple import config

from tests import APITestCase, APIClient
from tests.authentication.fixtures import AUTHENTICATION_FIXTURES
from tests.authentication.endpoints import AuthenticationEndpoints


class TestAuthenticationViews(APITestCase):
    fixtures = AUTHENTICATION_FIXTURES

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

        self.assertEqual(response.status_code, 200, msg="Login should succeed with valid credentials")

    def test_login_failure_with_invalid_username(self):
        response = self.client.post(
            path=self.endpoints.login,
            data={
                'username': "purposedly_invalid_username",
                'password': self.user_data['password'],
            },
            format="json"
        )

        self.assertEqual(response.status_code, 401, msg="Login should fail with invalid username")

    def test_login_failure_with_invalid_password(self):
        response = self.client.post(
            path=self.endpoints.login,
            data={
                'username': self.user_data['username'],
                'password': "purposedly_invalid_password",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 401, msg="Login should fail with invalid password")

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

        self.assertNotEqual(original_token, refreshed_token, msg="Token should be refreshed as long as the original is still valid")

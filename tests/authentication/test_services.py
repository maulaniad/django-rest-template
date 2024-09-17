from decouple import config
from freezegun import freeze_time
from jwt import decode, ExpiredSignatureError

from django.conf import settings
from django.utils.timezone import now, timedelta

from api.authentication.services import AuthService
from tests import APITestCase
from tests.authentication.fixtures import AUTHENTICATION_FIXTURES


class TestAuthenticationServices(APITestCase):
    fixtures = AUTHENTICATION_FIXTURES

    def setUp(self) -> None:
        self.service = AuthService
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_token_should_expire(self):
        token, _ = self.service.login(
            {
                'username': config('TEST_USERNAME', default=None, cast=str),
                'password': config('TEST_PASSWORD', default=None, cast=str)
            }
        )

        with freeze_time(now() + timedelta(hours=settings.JWT_EXP_HOURS)):
            try:
                decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                expired = False
            except ExpiredSignatureError:
                expired = True

        self.assertTrue(expired, msg="Token should be able to expire")

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
        settings.OTP_AUTH = False

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

    def test_otp_should_be_created(self):
        settings.OTP_AUTH = True

        access_id, _ = self.service.create_otp(
            {
                'username': config('TEST_USERNAME', default=None, cast=str),
                'password': config('TEST_PASSWORD', default=None, cast=str)
            }
        )

        self.assertIsNotNone(access_id, msg="OTP should be created")

    def test_otp_should_not_exceed_max_retries(self):
        settings.OTP_AUTH = True

        access_id, _ = self.service.create_otp(
            {
                'username': config('TEST_USERNAME', default=None, cast=str),
                'password': config('TEST_PASSWORD', default=None, cast=str)
            }
        )

        for _ in range(settings.OTP_MAX_RETRIES):
            access_id, _ = self.service.verify_otp(
                {
                    'access_id': access_id,
                    'otp': 12300
                }
            )

        self.assertIsNone(access_id, msg="OTP should not exceed max retries")

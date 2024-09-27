from typing import Any

from django.conf import settings

from api.authentication.serializers import UserDataSerializer
from core.authentication import authenticate
from helpers import Cache, Request
from helpers.types import EmailMessage
from helpers.utils import generate_token, generate_otp, send_email


class AuthService:
    @staticmethod
    def login(data: dict[str, Any]) -> tuple[str | Any, str | None]:
        username = data.get('username', None)
        password = data.get('password', None)

        user_data = authenticate(request=None, username=username, password=password)
        if not user_data:
            return None, "Invalid credentials"

        serializer = UserDataSerializer(user_data)
        encoded_token = generate_token(serializer.data)

        return encoded_token, None

    @staticmethod
    def refresh_token(request: Request) -> tuple[str | Any, str | None]:
        if not request.user.is_authenticated:
            return None, "User not authenticated"

        serializer = UserDataSerializer(request.user)
        encoded_token = generate_token(serializer.data)

        return encoded_token, None

    @staticmethod
    def create_otp(data: dict[str, Any]) -> tuple[str | Any, str | None]:
        username = data.get('username', None)
        password = data.get('password', None)

        user_data = authenticate(request=None, username=username, password=password)
        if not user_data:
            return None, "Invalid credentials"

        serializer = UserDataSerializer(user_data)
        encoded_token = generate_token(serializer.data)
        otp_code = generate_otp()

        Cache.set(f"token_{user_data.profile.oid}_{otp_code}", encoded_token)
        Cache.set(
            f"otp_{user_data.profile.oid}",
            {
                'otp': otp_code,
                'token': encoded_token,
                'retries': 0
            }
        )

        message = EmailMessage(
            subject="One Time Password - Django REST Framework",
            body=f"Your One Time Password is {otp_code}",
            to=[user_data.email],
        )
        send_email(message)
        return user_data.profile.oid, None

    @staticmethod
    def verify_otp(data: dict[str, Any]) -> tuple[str | Any, str | None]:
        access_id = data.get('access_id', None)
        otp_code = data.get('otp', None)

        cached_data = Cache.get(f"otp_{access_id}")
        if not cached_data:
            return None, "OTP has expired, please try again"

        if cached_data['retries'] >= settings.OTP_MAX_RETRIES:
            return None, "Max retries reached, please try login again"

        if cached_data['otp'] != otp_code:
            cached_data['retries'] += 1
            Cache.set(f"otp_{access_id}", cached_data)
            return None, "Invalid One Time Password"

        Cache.delete(f"otp_{access_id}")
        return cached_data['token'], None

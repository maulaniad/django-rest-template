from typing import Any

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
    def create_otp(data: dict[str, Any]) -> tuple[int | Any, str | None]:
        username = data.get('username', None)
        password = data.get('password', None)

        user_data = authenticate(request=None, username=username, password=password)
        if not user_data:
            return None, "Invalid credentials"

        serializer = UserDataSerializer(user_data)
        encoded_token = generate_token(serializer.data)
        otp_code = generate_otp()

        Cache.set(f"token_{user_data.profile.oid}_{otp_code}", encoded_token)
        Cache.set(f"otp_{user_data.profile.oid}", otp_code)

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

        cached_otp = Cache.get(f"otp_{access_id}")
        if cached_otp != otp_code:
            return False, "Invalid One Time Password"

        token = Cache.get(f"token_{access_id}_{cached_otp}")
        if not token:
            return None, "OTP has expired, please try again"

        Cache.delete(f"otp_{access_id}")
        Cache.delete(f"token_{access_id}_{cached_otp}")
        return token, None

from typing import Any

from django.contrib.auth import authenticate

from api.authentication.serializers import UserDataSerializer
from helpers import Request
from helpers.utils import generate_token


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

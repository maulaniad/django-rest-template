from jwt import encode
from typing import Any

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.timezone import now, timedelta

from api.authentication.serializers import UserDataSerializer
from database.repositories import UserRepo


class AuthService:
    repo = UserRepo()

    def login(self, data: dict[str, Any] | Any) -> tuple[Any, str | None]:
        username = data.get('username', None)
        password = data.get('password', None)
        time = now()

        user_data = authenticate(request=None, username=username, password=password)
        if not user_data:
            return None, "User not found"

        serializer = UserDataSerializer(user_data)
        encoded_token = encode(
            {
                **serializer.data,
                'exp': time + timedelta(hours=settings.JWT_EXP_HOURS, microseconds=time.microsecond),
            },
            key=settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_token, None

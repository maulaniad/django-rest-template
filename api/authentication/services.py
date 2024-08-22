from typing import Any

from django.contrib.auth.models import User


class AuthService():
    def login(self, data: dict[str, Any]) -> tuple[Any, str | None]:
        username = data.get('username', None)
        password = data.get('password', None)

        user_registered = User.objects.filter(
            username=username
        ).first()

        if not user_registered:
            return None, "User not found"

        if not user_registered.check_password(password):
            return None, "Wrong password"

        return None, None

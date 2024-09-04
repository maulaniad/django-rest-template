from typing import Any

from database.data.user import UserData
from database.data.profile import ProfileData

class AuthService:
    repo = UserData()

    def login(self, data: dict[str, Any] | Any) -> tuple[Any, str | None]:
        username = data.get('username', None)
        password = data.get('password', None)

        user_registered = self.repo.get_user_by_username(username)

        if not user_registered:
            return None, "User not found"

        if not user_registered.check_password(password):
            return None, "Wrong password"

        return None, None


class ProfileService:
    repo = ProfileData()

    def create_new_profile(self, data: dict[str, Any] | Any) -> tuple[Any, str | None]:
        data = self.repo.create_profile(**data)
        return data, None

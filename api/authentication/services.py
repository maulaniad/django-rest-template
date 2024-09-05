from typing import Any

from database.repositories import ProfileRepo, UserRepo


class AuthService:
    repo = UserRepo()

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
    repo = ProfileRepo()

    def create_new_profile(self, data: dict[str, Any] | Any) -> tuple[Any, str | None]:
        data = self.repo.create_profile(**data)
        return data, None

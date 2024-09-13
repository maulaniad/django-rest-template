from jwt import decode, ExpiredSignatureError, InvalidTokenError
from typing import Any

from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from database.repositories import UserRepo
from helpers import HttpError


class AuthenticationBackend(BaseBackend):
    repo = UserRepo

    def authenticate(self, request: HttpRequest, username=None, password=None, **kwargs):
        if not username or not password:
            raise HttpError._400_("Username and password are required to login")

        query = Q(username=username) | Q(email=username)
        user_data = self.repo.manager().filter(query).select_related('profile').first()

        if not user_data:
            return None

        if not check_password(password, user_data.password):
            return None

        if not user_data.is_active:
            raise HttpError._401_("User is not active")

        user_data.last_login = timezone.now()
        user_data.save()
        return user_data


class JWTAuthentication(BaseAuthentication):
    repo = UserRepo

    def authenticate(self, request: Request) -> tuple[Any, Any] | None:
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            raise HttpError._400_("No token provided")

        try:
            token = auth_header.split(" ")[1]
            payload = decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

            user = self.repo.get_user_by_username(username=payload['username'])
            if not user:
                raise HttpError._401_("User not registered")

            request.user = user
        except ExpiredSignatureError:
            raise HttpError._401_("Token expired")
        except (InvalidTokenError, KeyError):
            raise HttpError._400_("Invalid token")
        except IndexError:
            raise HttpError._400_("Invalid Bearer token format")

        return (request.user, None)

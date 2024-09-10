from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest
from django.utils import timezone

from helpers.exception import HttpError


class AuthenticationBackend(BaseBackend):
    def authenticate(self, request: HttpRequest | None = None, username=None, password=None, **kwargs):
        if not username or not password:
            raise HttpError._400_("Username and password are required to login")

        query = Q(username=username) | Q(email=username)
        user_data = User.objects.filter(query).select_related('profile').first()

        if not user_data:
            return None

        if not check_password(password, user_data.password):
            raise HttpError._400_("Wrong password")

        if not user_data.is_active:
            raise HttpError._401_("User is not active")

        user_data.last_login = timezone.now()
        user_data.save()
        return user_data

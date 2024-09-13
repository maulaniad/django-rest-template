from django.contrib.auth.models import User
from django.db.models import Q


class UserRepo:
    @staticmethod
    def get_users():
        return User.objects.all().select_related('profile')

    @staticmethod
    def get_user(id_or_oid: int | str):
        return User.objects.filter(
            Q(id=id_or_oid) | Q(oid=id_or_oid)
        ).select_related('profile').first()

    @staticmethod
    def get_user_by_email(email: str):
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_user_by_username(username: str):
        return User.objects.filter(username=username).first()

    @staticmethod
    def manager():
        return User.objects

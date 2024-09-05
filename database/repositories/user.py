from django.db.models import Q
from django.contrib.auth.models import User


class UserRepo:
    def get_users(self):
        return User.objects.all().select_related('profile')

    def get_user(self, id_or_oid: int | str):
        return User.objects.filter(
            Q(id=id_or_oid) | Q(oid=id_or_oid)
        ).select_related('profile').first()

    def get_user_by_email(self, email: str):
        return User.objects.filter(email=email).first()

    def get_user_by_username(self, username: str):
        return User.objects.filter(username=username).first()

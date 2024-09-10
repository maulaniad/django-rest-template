from django.db.models import Q

from database.models import Profile


class ProfileRepo:
    def get_profiles(self):
        return Profile.objects.select_related('user').all()

    def get_profile(self, id_or_oid: int | str):
        return Profile.objects.filter(Q(id=id_or_oid) | Q(oid=id_or_oid)).select_related('user').first()

    def get_profile_by_user_id(self, user_id: int):
        return Profile.objects.filter(user=user_id).select_related('user').first()

    def create_profile(self, name: str, email: str, user_id: int, asset: int | str, profit: int | str):
        data = Profile.objects.create(
            name=name,
            email=email,
            user_id=user_id,
            asset=asset,
            profit=profit
        )

        return data

    def manager(self):
        return Profile.objects

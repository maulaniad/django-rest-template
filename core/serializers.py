from rest_framework.serializers import Serializer, CharField, BooleanField, DateTimeField


class UserProfileDataSerializer(Serializer):
    oid = CharField(max_length=21)
    date_created = DateTimeField()
    date_updated = DateTimeField()
    date_deleted = DateTimeField(allow_null=True)
    name = CharField(max_length=50, allow_blank=True)
    phone = CharField(max_length=15, allow_blank=True)


class UserDataSerializer(Serializer):
    username = CharField(max_length=50, required=True)
    email = CharField(max_length=50, required=True)
    is_active = BooleanField(default=True)
    last_login = DateTimeField(allow_null=True)
    profile = UserProfileDataSerializer()

from rest_framework.serializers import (Serializer,
                                        ModelSerializer,
                                        BooleanField,
                                        CharField,
                                        DateTimeField,
                                        IntegerField)


class ValidateLoginPayload(Serializer):
    username = CharField(max_length=50, required=True)
    password = CharField(required=True)


class ValidateVerifyOTPPayload(Serializer):
    access_id = CharField(max_length=21, required=True)
    otp = IntegerField(required=True)


class ProfileDataSerializer(ModelSerializer):
    oid = CharField(max_length=21)
    date_created = DateTimeField()
    date_updated = DateTimeField()
    date_deleted = DateTimeField(allow_null=True)
    name = CharField(max_length=50, allow_blank=True)
    phone = CharField(max_length=15, allow_blank=True)


class UserDataSerializer(ModelSerializer):
    username = CharField(max_length=50, required=True)
    email = CharField(max_length=50, required=True)
    is_active = BooleanField(default=True)
    last_login = DateTimeField(allow_null=True)
    profile = ProfileDataSerializer()

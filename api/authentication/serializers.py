from rest_framework.serializers import (ALL_FIELDS,
                                        Serializer,
                                        ModelSerializer,
                                        CharField,
                                        IntegerField,
                                        DecimalField)

from database.models import Profile


class LoginPayloadSerializer(Serializer):
    username = CharField(max_length=50, required=True)
    password = CharField(required=True)


class CreateProfileSerializer(Serializer):
    name = CharField(max_length=50, required=True)
    email = CharField(max_length=50, required=True)
    user_id = IntegerField(required=True)
    asset = DecimalField(max_digits=20, decimal_places=0)
    profit = DecimalField(max_digits=20, decimal_places=0)


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ALL_FIELDS

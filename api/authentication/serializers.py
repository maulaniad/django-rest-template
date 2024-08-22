from rest_framework.serializers import Serializer, CharField


class LoginPayloadSerializer(Serializer):
    username = CharField(max_length=50, required=True)
    password = CharField(required=True)

from rest_framework.generics import GenericAPIView

from api.authentication.serializers import (LoginPayloadSerializer,
                                            CreateProfileSerializer,
                                            ProfileSerializer)
from api.authentication.services import AuthService, ProfileService
from helpers import HttpError, Request, Response


class LoginView(GenericAPIView):
    service = AuthService()

    def post(self, request: Request, *args, **kwargs):
        payload = LoginPayloadSerializer(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        _, error = self.service.login(payload.data)

        if error:
            raise HttpError._400_(error)

        return Response({'token': "XYZ123ABC"})


class ProfileView(GenericAPIView):
    service = ProfileService()

    def post(self, request: Request, *args, **kwargs):
        payload = CreateProfileSerializer(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        data, error = self.service.create_new_profile(payload.data)

        if error:
            raise HttpError._400_(error)

        serialized_data = ProfileSerializer(data)
        return Response(serialized_data.data)

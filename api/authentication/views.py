from rest_framework.generics import GenericAPIView

from api.authentication.serializers import LoginPayloadSerializer
from api.authentication.services import AuthService
from helpers import HttpError, Request, Response


class LoginView(GenericAPIView):
    service = AuthService()

    def post(self, request: Request, *args, **kwargs):
        payload = LoginPayloadSerializer(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        token, error = self.service.login(payload.data)

        if error:
            raise HttpError._400_(error)

        return Response({'token': token}, message="Authenticated")

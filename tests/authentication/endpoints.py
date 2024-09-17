from django.urls import reverse


class AuthenticationEndpoints:
    login = reverse("authentication:login")
    refresh_token = reverse("authentication:refresh-token")

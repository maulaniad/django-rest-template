from django.urls import path

from api.authentication.views import LoginView, RefreshTokenView


app_name = "authentication"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("refresh-token", RefreshTokenView.as_view(), name="refresh-token")
]

from django.urls import path

from api.authentication.views import LoginView, ProfileView


app_name = "authentication"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("create-profile/", ProfileView.as_view(), name="profile")
]

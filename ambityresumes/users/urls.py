from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import AccountView, AuthView

app_name = "users"

urlpatterns = [
    path(
        "auth/",
        AuthView.as_view(),
        name="auth",
    ),
    path(
        "account/",
        AccountView.as_view(),
        name="account",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]

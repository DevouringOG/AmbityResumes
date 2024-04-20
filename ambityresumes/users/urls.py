from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import AuthView, AccountView

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

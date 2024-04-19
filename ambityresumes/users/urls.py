from django.urls import path
from django.contrib.auth.views import LogoutView

import users.views

app_name = "users"

urlpatterns = [
    path(
        "auth/",
        users.views.AuthView.as_view(),
        name="auth",
    ),
    path(
        "account/",
        users.views.AccountView.as_view(),
        name="account",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]

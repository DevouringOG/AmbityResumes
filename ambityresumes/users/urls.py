from django.urls import path

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
]

from re import template
import django
from django.urls import include, path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from users.views import password_reset_request, register_user

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("register", register_user, name="register"),
    path("password_reset", password_reset_request, name="password-reset"),
    path(
        "password_reset_done",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_sent.html"
        ),
        name="password-reset-done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm_template.html",
            success_url='/reset/done'
        ),
        name="password-reset-confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_confirm_done_template.html"
        ),
        name="password-reset-confirm-done",
    ),
]

"""
Site urls that live under /profile/
"""
################################################################

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from ..forms import StrengthCheckPasswordChangeForm, StrengthCheckSetPasswordForm

################################################################

urlpatterns = [
    url(
        "^$",
        login_required(TemplateView.as_view(template_name="registration/profile.html")),
        name="user-profile",
    ),
    url(
        "^password-change/$",
        auth_views.PasswordChangeView.as_view(),
        kwargs={"password_change_form": StrengthCheckPasswordChangeForm},
        name="password_change",
    ),
    url(
        "^password-change/done/$",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    url(
        "^password-reset/$",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    url(
        "^password-reset/done/$",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_reset_done",
    ),
    url(
        "^password-reset/confirm/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(),
        kwargs={"set_password_form": StrengthCheckSetPasswordForm},
        name="password_reset_confirm",
    ),
    url(
        "^password-reset/complete/$",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_confirm",
    ),
]

################################################################

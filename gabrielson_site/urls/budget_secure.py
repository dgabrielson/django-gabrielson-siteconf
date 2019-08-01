"""
The url patterns for the budget application.
"""
from functools import partial

from django.conf.urls import include, patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from ..decorators import decorated_patterns, secure_required

urlpatterns = decorated_patterns(
    secure_required,
    patterns(
        "",
        url(
            r"^login/$",
            "django.contrib.auth.views.login",
            kwargs={"template_name": "budget/login.html"},
            name="budget-login",
        ),
    ),
)

urlpatterns += decorated_patterns(
    (secure_required, partial(login_required, login_url=reverse_lazy("budget-login"))),
    patterns("", url("^", include("budget.urls"))),
)

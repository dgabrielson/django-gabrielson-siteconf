from admin_export.actions import export_redirect_spreadsheet_xlsx
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.static import serve as static_serve

from ..decorators import decorated_patterns, secure_required

admin.autodiscover()

site.add_action(export_redirect_spreadsheet_xlsx)


# from django.conf import settings
# if getattr(settings, 'DEBUG', False):
#     import warnings
#     warnings.simplefilter('error', DeprecationWarning)

urlpatterns = decorated_patterns(
    secure_required,
    [
        url(r"^login/$", auth_views.LoginView.as_view(), name="site-login"),
        url(r"^profile/", include("gabrielson_site.urls.profile")),
        url(r"^ctl/$", RedirectView.as_view(url="/administration/", permanent=True)),
        url(r"^administration/export/", include("admin_export.urls")),
        url(r"^administration/", admin.site.urls),
    ],
)


urlpatterns += [
    # This will never get called in the production site
    url(r"^media/(.*)$", static_serve, kwargs={"document_root": settings.MEDIA_ROOT}),
    url(
        r"^logout/$",
        auth_views.LogoutView.as_view(),
        kwargs={"next_page": "/"},
        name="site-logout",
    ),
    url(r"^search/", include("haystack.urls")),
    url(
        r"^whats-my-address$",
        TemplateView.as_view(template_name="whats_my_address.html"),
        name="whats-my-address",
    ),
    url(
        r"^whats-my-address-test$",
        TemplateView.as_view(template_name="whats_my_address_test.html"),
        name="whats-my-address-test",
    ),
    url(
        r"^lorem-ipsum$",
        TemplateView.as_view(template_name="lorem-ipsum.html"),
        name="lorem-ipsum",
    ),
    url(r"^xkcd/", include("xkcd.urls")),
    url(r"^aquarium/", include("aquainfo.urls")),
    url(r"^diet/", include("diet.urls")),
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="site-index"),
]

# Extend with debug patterns.
if getattr(settings, "DEBUG", False):
    urlpatterns += [
        url(r"^debug$", TemplateView.as_view(template_name="debug.html"), name="debug")
    ]

from __future__ import print_function, unicode_literals

#######################
#######################
import warnings


def finalize_settings(settings):
    """
    Call finalize settings at the top level scope as
    locals().update(finalize_settings(locals()))
    """
    updates = {}

    #########################################################
    #
    # Finally, do any alterations that need to occur after
    #   all settings have been set.
    #
    #########################################################

    # Make sure that manage.py runserver can do auth.
    if settings["DEBUG"]:
        updates["SESSION_COOKIE_SECURE"] = False

    #########################################################
    # Enable template caching when DEBUG=False
    # NOTE: b/c we are modifying the TEMPLATES dictionary in place,
    #   it does not need to be returned via updates.
    if not settings["DEBUG"]:
        for t in settings["TEMPLATES"]:
            if "OPTIONS" in t and "loaders" in t["OPTIONS"]:
                t["OPTIONS"]["loaders"] = [
                    ("django.template.loaders.cached.Loader", t["OPTIONS"]["loaders"])
                ]

    #########################################################
    # Alter warning behaviour
    if not settings["DEBUG"]:
        # Ignore Deprecation and User warnings in production.
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
    else:
        # Make USE_TZ warnings into errors for testing.
        warnings.filterwarnings(
            "error",
            r"DateTimeField received a naive datetime",
            RuntimeWarning,
            r"django\.db\.models\.fields",
        )

    #########################################################
    # Debug toolbar:
    if settings["DEBUG"] and settings.get("USE_DEBUG_TOOLBAR", False):
        updates["INSTALLED_APPS"] = list(settings["INSTALLED_APPS"]) + ["debug_toolbar"]
        updates["DEBUG_TOOLBAR_PATCH_SETTINGS"] = False
        updates["INSTALLED_APPS"] = list(settings["INSTALLED_APPS"]) + ["debug_toolbar"]
        updates["INTERNAL_IPS"] = ["127.0.0.1"]
        updates["MIDDLEWARE"] = settings["MIDDLEWARE"] + [
            "debug_toolbar.middleware.DebugToolbarMiddleware"
        ]

    #########################################################
    #########################################################
    #########################################################

    return updates

"""
LOGGING setting for site.
"""
#######################################################################

from django.core.exceptions import DisallowedHost
from django.http import UnreadablePostError

#######################################################################


def skip_unreadable_post(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        if isinstance(exc_value, UnreadablePostError):
            return False
    return True


#######################################################################


def skip_disallowed_host(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        if isinstance(exc_value, DisallowedHost):
            return False
    return True


#######################################################################

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "skip_unreadable_posts": {
            "()": "django.utils.log.CallbackFilter",
            "callback": skip_unreadable_post,
        },
    },
    "handlers": {
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false", "skip_unreadable_posts"],
            "level": "ERROR",
        }
    },
    "loggers": {
        #                 'django.security.DisallowedHost': {
        #                     'handlers': ['null'],
        #                     'propagate': False,
        #                 },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        }
    },
}

#######################################################################

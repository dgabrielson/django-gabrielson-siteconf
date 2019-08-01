"""
Decorators for the gabrielson site.
"""
from django.conf import settings
from django.http import HttpResponseRedirect

HTTPS_ENABLED = getattr(settings, "HTTPS_ENABLED", False)

# HTTPS_ENABLED = True should be set in local_settings.py


def secure_required(view_func):
    """
    Decorator makes sure URL is accessed over ssl.
    """

    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if HTTPS_ENABLED:
                url = request.build_absolute_uri(request.get_full_path())
                ssl_url = url.replace("http://", "https://")
                return HttpResponseRedirect(ssl_url)
        return view_func(request, *args, **kwargs)

    # set a nice doc string
    _wrapped_view_func.__doc__ = ""
    if view_func.__doc__ is not None:
        _wrapped_view_func.__doc__ += view_func.__doc__ + "\n"
    _wrapped_view_func.__doc__ += "[Wrapped by secure_required]"

    return _wrapped_view_func


def decorated_patterns(wrapping_functions, patterns_rslt):
    """
    Used to require 1..n decorators in any view returned by a url tree

    Usage:
      urlpatterns = decorated_patterns(func, patterns(...))
      urlpatterns = decorated_patterns((func, func, func), patterns(...))

    Example:
        urlpatterns += decorated_patterns(
            login_required,
            [
                url(r'^private/', include('private.urls')),
            ]
        )

    Note:
      If you need to pass args to a decorator you will have to
      write a wrapper function.
      Use functools.partial to pass keyword params to the required
      decorators.

    Example:
        from functools import partial

        urlpatterns = decorated_patterns(
            partial(login_required, login_url='/accounts/login/'),
            patterns(...)
        )

    Source:
        http://stackoverflow.com/questions/2307926/is-it-possible-to-decorate-include-in-django-urls-with-login-required
    """

    def _wrap_instance__resolve(wrapping_functions, instance):
        """
        Wrap an single resolver instance.
        """

        def _wrap_func_in_returned_resolver_match(*args, **kwargs):
            """
            Wrap a function in a resolver match.
            """
            rslt = resolve(*args, **kwargs)
            if not hasattr(rslt, "func"):
                return rslt
            f = getattr(rslt, "func")
            for _decorater in reversed(wrapping_functions):
                # @decorate the function from inner to outer
                f = _decorater(f)
            setattr(rslt, "func", f)
            return rslt

        # _wrap_instance__resolve() begins
        if not hasattr(instance, "resolve"):
            return instance
        resolve = getattr(instance, "resolve")
        setattr(instance, "resolve", _wrap_func_in_returned_resolver_match)
        return instance

    # decorated_patterns() begins
    if not hasattr(wrapping_functions, "__iter__"):
        wrapping_functions = (wrapping_functions,)
    return [
        _wrap_instance__resolve(wrapping_functions, instance)
        for instance in patterns_rslt
    ]

"""
Forms that take advantage of django-passwords application field
"""
################################################################

from collections import OrderedDict

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _

# django-passwords
from passwords.fields import PasswordField

################################################################


class StrengthCheckSetPasswordForm(SetPasswordForm):
    """
    Use the django-passwords PasswordField
    """

    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))


################################################################


class StrengthCheckPasswordChangeForm(PasswordChangeForm):
    """
    Use the django-passwords PasswordField
    """

    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))


StrengthCheckPasswordChangeForm.base_fields = OrderedDict(
    [
        (k, StrengthCheckPasswordChangeForm.base_fields[k])
        for k in ["old_password", "new_password1", "new_password2"]
    ]
)

################################################################

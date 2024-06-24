from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _


class UserNotActive(AuthenticationFailed):
    default_detail = _('Your account is temporarily disabled, contact your manager!')
    default_code = 'authentication_failed'


class UserCredentialsInvalid(AuthenticationFailed):
    default_detail = _('The entered email or password is incorrect!')
    default_code = 'authentication_failed'


class UserNotFound(AuthenticationFailed):
    default_detail = _('Unfortunately, you are not registered in our system!')
    default_code = 'authentication_failed'


class UserPasswordNotSet(AuthenticationFailed):
    default_detail = _('Please recover your password!')
    default_code = 'authentication_failed'


class UserEmailSettingsFailed(AuthenticationFailed):
    default_detail = _("Didn't install full SMTP settings!")
    default_code = 'authentication_failed'

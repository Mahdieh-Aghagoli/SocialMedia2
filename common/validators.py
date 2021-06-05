import re

from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

USERNAME_PATTERN = '^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'


def username_validator(name):
    if not re.search(USERNAME_PATTERN, name):
        raise ValidationError(_('Invalid name'))

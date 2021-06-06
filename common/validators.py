import re

from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

USERNAME_PATTERN = '^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
WEBSITE_PATTERN = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'


def username_validator(username):
    if not re.search(USERNAME_PATTERN, username):
        raise ValidationError(_('Invalid username'))


def phone_validator(phone):
    if not re.search('^(09[0-9]{9})$', phone):
        raise ValidationError(_('Invalid phone number'))


def website_validator(website):
    if not re.search(WEBSITE_PATTERN, website):
        raise ValidationError(_('Invalid website address'))

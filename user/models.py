from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from common.validators import username_validator
from user.managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), max_length=30, unique=True,)
    email = models.EmailField(_('Email'), blank=True, null=True, unique=True)
    phone = models.CharField(_('Phone number'), max_length=11, blank=True, null=True, unique=True,
                             validators=[])
    bio = models.TextField(_('Bio'), blank=True, max_length=100)
    GENDER_CHOICES = [('N', _('None')),
                      ('F', _('Female')),
                      ('M', _('Male'))]
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(_('Birthday'), blank=True, null=True,
                                help_text=_('Please use the follow format :<em>YYYY-MM-DD</em>'))
    website = models.CharField(_('Website'), blank=True, max_length=150, validators=[])
    avatar = models.ImageField(blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_superuser = models.BooleanField(_('Superuser'), default=False)
    is_staff = models.BooleanField(_('Staff'), default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from user.models import Account


class SignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('email') is None and cleaned_data.get('phone') is None:
            self._errors['email'] = self._errors.get('email', [])
            self._errors['email'].append(_('Please Enter Email or Phone number'))
        return cleaned_data

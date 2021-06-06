import pyotp as pyotp
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import UpdateView
from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse

from user.forms import UserRegisterForm, UserUpdateForm
from user.models import Account
from user.tokens import account_activation_token

activate('fa')


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        verification_way = request.POST.get('verification')
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if form.cleaned_data['phone'] and form.cleaned_data['email'] and verification_way:
                return redirect(reverse('send-email', args=(user.slug,)))
            elif form.cleaned_data['phone']:
                return redirect(reverse('send-sms', args=(user.slug,)))
            else:
                return redirect(reverse('send-email', args=(user.slug,)))
        return render(request, 'user/register.html', {'form': form})


class SendEmailVCode(View):
    def get(self, request, user_slug):
        user = get_object_or_404(Account, slug=user_slug)
        current_site = get_current_site(request)
        mail_subject = 'Activate SocialMedia account.'
        message = render_to_string('user/email_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
            'token': account_activation_token.make_token(user),
        })

        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(request, 'user/email_waiting.html', {'user': user})


class EmailVerify(View):
    def get(self, request, uidb64, token):
        try:

            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse('login'))
        else:
            return HttpResponse(_('Activation link is invalid!'))


class SendSmsVerification(View):
    def get(self, request, user_slug):
        try:
            api = KavenegarAPI(
                '485A50392B30394471492F6C4C344E58527A6E43314A3166766633446E445974494E473650744B7A6171673D')
            user = get_object_or_404(Account, slug=user_slug)
            time_otp = pyotp.TOTP(user.otp, interval=120)
            time_otp = time_otp.now()
            print(time_otp)
            params = {
                'sender': '1000596446',  # optional
                'receptor': user.phone,  # multiple mobile number, split by comma
                'message': 'Your code is {}'.format(time_otp),
            }
            response = api.sms_send(params)
            print('key: ', time_otp)
            print(response)
            return redirect(reverse('sms-verify', args=(user.slug,)))
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)


class SmsVerify(View):
    def get(self, request, user_slug):
        user = get_object_or_404(Account, slug=user_slug)
        return render(request, 'user/smsVerify.html', {'user': user})

    def post(self, request, user_slug):
        user = get_object_or_404(Account, slug=user_slug)
        code = request.POST.get('code')
        if user.authenticate(code):
            user.is_active = True
            user.save()
            return redirect(reverse('login'))

        return render(request, 'user/smsVerify.html', {'user': user})


class ProfileView(UpdateView):
    model = Account
    form_class = UserUpdateForm
    template_name = 'user/profile.html'

    def get_success_url(self):
        return reverse('profile')

    def get_object(self, **kwargs):
        return self.request.user


class AutocompleteSearch(View):
    def get(self, request, slug):
        if 'term' in request.GET:
            qs = Account.objects.exclude(slug=slug).filter(username__icontains=request.GET.get('term'))
            search_result = []
            for user in qs:
                search_result.append(user.slug)
            return JsonResponse(search_result, safe=False)
        return render(request, 'user/search.html')

from django.contrib.auth import views as v
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('login/', v.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(), name='logout'),

    re_path(r'send-email/(?P<user_slug>[-\w]+)/', SendEmailVCode.as_view(), name='send-email'),
    path('emailVerify/<uidb64>/<token>/', EmailVerify.as_view(), name='emailVerify'),
    re_path(r'send-sms/(?P<user_slug>[-\w]+)/', SendSmsVerification.as_view(), name='send-sms'),
    re_path(r'mobile_verify/(?P<user_slug>[-\w]+)/', SmsVerify.as_view(), name='smsVerify'),

    re_path(r'search/(?P<slug>[-\w]+)/', AutocompleteSearch.as_view(), name='search'),

    re_path(r'edit_profile/(?P<slug>[-\w]+)/', ProfileView.as_view(), name='edit_profile'),

    path('password_change/', v.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', v.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', v.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', v.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', v.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', v.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

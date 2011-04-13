# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail


class RegistrationForm(RegistrationFormUniqueEmail):

    error_css_class = 'error'
    required_css_class = 'required'

    title = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=30, required=True, label='* First name')
    last_name = forms.CharField(max_length=30,required=True, label='* Last name')

    organization_name = forms.CharField(required=True, label='* Organization name')
    organization_sector = forms.CharField(widget=(forms.Select(attrs={'class':'width-200px'},choices=(('PublicHealth', 'Public Health'),('Other', 'Other'),))))
    organization_addressline1 = forms.CharField(required=True,max_length=30,label='* Address Line 1')
    organization_addressline2 = forms.CharField(max_length=30, required=False, label='Address Line 2')
    organization_city = forms.CharField(max_length=30,required=True, label='* City')
    organization_state = forms.CharField(max_length=30, required=False, label='State / Province')
    organization_country = forms.CharField(max_length=30,required=True, label='* Country')
    organization_zipcode = forms.CharField(max_length=30,required=True, label='* Postal / Zip Code')
    organization_office_phone = forms.CharField(max_length=30, required=False, label='Office Phone Number')
    organization_website = forms.URLField(required=False, label='Website Url')
    username = forms.CharField(max_length=30, required=False)

    def clean_email(self):
        super(RegistrationForm, self).clean_email()
        email = self.cleaned_data.get('email')
        self.cleaned_data['email'] = email.lower()
        return self.cleaned_data['email']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                msg = "The two password fields didn't match."
                self._errors['password1'] = self.error_class([msg])
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    error_css_class = 'error'
    required_css_class = 'required'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        self.cleaned_data['username'] = username.lower()
        return self.cleaned_data['username']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        self.check_for_test_cookie()
        return self.cleaned_data


class ResetPasswordForm(PasswordResetForm):
    error_css_class = 'error'
    required_css_class = 'required'

class PasswordSetForm(SetPasswordForm):
    error_css_class = 'error'
    required_css_class = 'required'




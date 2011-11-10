# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from datawinners.entity.fields import PhoneNumberField
from mangrove.errors.MangroveException import TrialAccountExpiredException
from models import  Organization
from django.contrib.auth.models import User


def get_organization_sectors():
    return (('', _('Please Select...')),
            ('CommercialBusiness', _('Commercial Business')),
            ('Education', _('Education')),
            ('Finance', _('Finance')),
            ('FoodSecurity', _('Food Security')),
            ('Health', _('Health')),
            ('HumanRights', _('Human Rights')),
            ('Shelter', _('Shelter')),
            ('WaterSanitation', _('Water and Sanitation')),
            ('Other', _('Other')))

class OrganizationForm(ModelForm):
    required_css_class = 'required'

    name = forms.CharField(required=True, label=_('Organization name'))
    sector = forms.CharField(required=False, widget=(
        forms.Select(attrs={'class': 'width-200px'}, choices=get_organization_sectors())),
                             label=_('Organization Sector'))
    address = forms.CharField(required=True, max_length=30, label=_('Address'))
    city = forms.CharField(max_length=30, required=True, label=_('City'))
    state = forms.CharField(max_length=30, required=False, label=_('State / Province'))
    country = forms.CharField(max_length=30, required=True, label=_('Country'))
    zipcode = forms.CharField(max_length=30, required=True, label=_('Postal / Zip Code'))
    office_phone = PhoneNumberField(required = False, label=_("Office Phone Number"))
    website = forms.URLField(required=False, label=_('Website Url'))

    class Meta:
        model = Organization


    def update(self):
        if self.is_valid():
            self.save()

        return self


class UserProfileForm(forms.Form):
    required_css_class = 'required'

    title = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=30, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Last name'))
    username = forms.EmailField(max_length=30, required=True, label=_("Email"), error_messages={
        'invalid': _('Enter a valid email address. Example:name@organization.com')})
    mobile_phone = PhoneNumberField(required = False, label=_("Mobile Phone"))
    office_phone = PhoneNumberField(required = False, label=_("Office Phone"))
    skype = forms.CharField(max_length=30, required=False, label="Skype")


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError(_("This email address is already in use. Please supply a different email address"))
        return self.cleaned_data.get('username')


class EditUserProfileForm(UserProfileForm):
    def clean_username(self):
        return self.cleaned_data.get('username')

class MinimalRegistrationForm(RegistrationFormUniqueEmail):
    required_css_class = 'required'

    title = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict({'class': 'required'},
                                                                                    maxlength=75)),
                             label=_("Email address"),
                             error_messages={
                                 'invalid': _('Enter a valid email address. Example:name@organization.com')})
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False),
                                label=_("Password (again)"))

    first_name = forms.CharField(max_length=30, required=True, label='First name')
    last_name = forms.CharField(max_length=30, required=True, label='Last name')
    office_phone = PhoneNumberField(required = False, label=_("Office Phone"))
    mobile_phone = PhoneNumberField(required = False, label=_("Mobile Phone"))
    organization_name = forms.CharField(required=True, max_length=30, label=_('Organization Name'))
    organization_sector = forms.CharField(required=False, widget=(
        forms.Select(attrs={'class': 'width-200px'}, choices=get_organization_sectors())),
                                          label=_('Organization Sector'))
    organization_city = forms.CharField(max_length=30, required=True, label=_('City'))
    organization_country = forms.CharField(max_length=30, required=True, label=_('Country'))
    username = forms.CharField(max_length=30, required=False)

    def clean(self):
        self.convert_email_to_lowercase()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                msg = _("The two password fields didn't match.")
                self._errors['password1'] = self.error_class([msg])
        return self.cleaned_data

    def convert_email_to_lowercase(self):
        email = self.cleaned_data.get('email')
        if email is not None:
            self.cleaned_data['email'] = email.lower()


def payment_details_form():
    pay_monthly = ('pay_monthly', _(mark_safe(
        "<div class='radio_title'>Monthly: $ 850 per month</div><div class='subtitle_for_radio_button'>Renews automatically each month<div>")))
    pay_half_yearly = ('half_yearly', _(mark_safe(
        "<div class='radio_title'>6 months:$ 765 per month</div><div class='subtitle_for_radio_button'>Save 10% by paying 6 months in advance</div> ")))
    INVOICE_PERIOD_CHOICES = (pay_monthly, pay_half_yearly)

    wire_transfer = ('wire_transfer', _(mark_safe("<div class='radio_title'>Wire transfer</div><div class='subtitle_for_radio_button'></div>")))
    credit_card = ('credit_card', _(mark_safe(
        "<div class='radio_title'>Credit card</div><div class='subtitle_for_radio_button'>Call us directly and we can securely process your credit card payment over the phone</div>")))
    pay_via_ach = ('pay_via_ach', _(mark_safe(
        "<div class='radio_title'>Pay via ACH</div><div class='subtitle_for_radio_button'>Securely transfer funds between your US-based bank account and ours (normally free of charge).</div>")))
    PREFERRED_PAYMENT_CHOICES = (wire_transfer, credit_card, pay_via_ach)

    invoice_period = forms.ChoiceField(required=True, label=_('Invoice Period'), widget=forms.RadioSelect,
                                       choices=INVOICE_PERIOD_CHOICES, initial='pay_monthly', help_text="O, no, Help")

    preferred_payment = forms.ChoiceField(required=False, label=_('Preferred Payment'), widget=forms.RadioSelect,
                                          choices=PREFERRED_PAYMENT_CHOICES, initial=False)

    return invoice_period, preferred_payment


class FullRegistrationForm(MinimalRegistrationForm):
    skype = forms.CharField(max_length=30, required=False, label="Skype")
    organization_address = forms.CharField(required=True, max_length=30, label=_('Address'))
    organization_state = forms.CharField(max_length=30, required=False, label=_('State / Province'))
    organization_zipcode = forms.RegexField(required=True, max_length=30, regex="^[a-zA-Z\d-]*$",
                                            error_message=_("Please enter a valid Postal / Zip code"),
                                            label=_('Postal / Zip Code'))
    organization_office_phone = PhoneNumberField(required = False, label=_("Office Phone Number"))
    organization_website = forms.URLField(required=False, label=_('Website Url'))

    invoice_period, preferred_payment = payment_details_form()


class LoginForm(AuthenticationForm):
    required_css_class = 'required'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        self.cleaned_data['username'] = username.lower()
        return self.cleaned_data['username']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.check_for_username_and_password(password, username)
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_username_and_password(self, password, username):
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct email and password."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

            self.check_trial_account_expired()

    def check_trial_account_expired(self):
        org = Organization.objects.get(org_id=self.user_cache.get_profile().org_id)
        if org.is_expired():
            raise TrialAccountExpiredException()


class ResetPasswordForm(PasswordResetForm):
    required_css_class = 'required'


class PasswordSetForm(SetPasswordForm):
    required_css_class = 'required'

class UpgradeForm(forms.Form):
    invoice_period, preferred_payment = payment_details_form()

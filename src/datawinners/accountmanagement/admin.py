# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User, Group
from registration.models import RegistrationProfile
from datawinners.accountmanagement.models import OrganizationSetting, SMSC, PaymentDetails, MessageTracker, Organization, NGOUserProfile
from mangrove.utils.types import is_empty, is_not_empty

admin.site.disable_action('delete_selected')

class DatawinnerAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class OrganizationSettingAdmin(DatawinnerAdmin):
    list_display = ('organization_name', 'organization_id', 'type', 'payment_details', 'activation_date')
    fields = ('sms_tel_number', 'smsc')

    def organization_name(self, obj):
        return obj.organization.name

    def organization_id(self, obj):
        return obj.organization.org_id

    def payment_details(self, obj):
        organization = obj.organization
        payment_details = PaymentDetails.objects.filter(organization = organization)
        if not is_empty(payment_details):
            return payment_details[0].preferred_payment

        return "--"

    def type(self, obj):
        return 'Trial' if obj.organization.in_trial_mode else 'Paid'

    def activation_date(self, obj):
        return obj.organization.active_date if obj.organization.active_date is not None else '--'


class MessageTrackerAdmin(DatawinnerAdmin):
    list_display = ("organization_name", "month", "incoming_messages", "outgoing_messages", "total_messages")

    def organization_name(self, obj):
        return obj.organization.name

    def month(self, obj):
        return obj.month

    def incoming_messages(self, obj):
        return obj.incoming_sms_count

    def outgoing_messages(self, obj):
        return obj.outgoing_sms_count

    def total_messages(self, obj):
        return obj.incoming_sms_count + obj.outgoing_sms_count


class OrganizationAdmin(DatawinnerAdmin):
    list_display = ('organization_name', 'complete_address', 'office_phone', 'website', 'paid', 'active_date','admin_name','admin_email','admin_mobile_number','admin_office_phone')

    def organization_name(self, obj):
        return obj.name

    def paid(self, obj):
        return "No" if obj.in_trial_mode else "Yes"

    def _get_ngo_admin(self, organization):
        user_profiles = NGOUserProfile.objects.filter(org_id=organization.org_id)
        admin_users = [x.user for x in user_profiles if x.user.groups.filter(name="NGO Admins")]
        #right now there is only one ngo admin
        return admin_users[0] if is_not_empty(admin_users) else NullAdmin()

    def admin_email(self, obj):
        return self._get_ngo_admin(obj).email

    def admin_office_phone(self, obj):
        admin_user = self._get_ngo_admin(obj)
        return admin_user.get_profile().office_phone

    def admin_mobile_number(self, obj):
        admin_user = self._get_ngo_admin(obj)
        return admin_user.get_profile().mobile_phone

    def admin_name(self, obj):
        admin_user = self._get_ngo_admin(obj)
        return self._get_full_name(admin_user)

    def complete_address(self, obj):
        complete_address = [obj.address, obj.addressline2, obj.city, obj.zipcode, obj.state, obj.country]
        return ", ".join([element for element in complete_address if is_not_empty(element)])

    def _get_full_name(self,user):
        return user.first_name + ' ' + user.last_name


class NullAdmin:
    def __init__(self):
        self.email=''
        self.mobile_phone=''
        self.office_phone=''
        self.first_name=''
        self.last_name=''

    def get_profile(self):
        return self


admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(OrganizationSetting, OrganizationSettingAdmin)
admin.site.register(SMSC,DatawinnerAdmin)
admin.site.register(MessageTracker, MessageTrackerAdmin)
admin.site.register(Organization, OrganizationAdmin)
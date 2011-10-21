# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datawinners import settings

from django.contrib.auth.models import  User
from django.db import models
from django.template.defaultfilters import slugify
from datawinners.accountmanagement.organization_id_creator import OrganizationIdCreator

class Organization(models.Model):
    name = models.TextField()
    sector = models.TextField()
    address = models.TextField()
    addressline2 = models.TextField(blank=True)
    city = models.TextField()
    state = models.TextField(blank=True)
    country = models.TextField()
    zipcode = models.TextField()
    office_phone = models.TextField(blank=True)
    website = models.TextField(blank=True)
    org_id = models.TextField(primary_key=True)
    in_trial_mode = models.BooleanField(False)
 
    @classmethod
    def create_organization(cls, org_details):
        organization = Organization(name=org_details.get('organization_name'),
                                sector=org_details.get('organization_sector'),
                                address=org_details.get('organization_address'),
                                city=org_details.get('organization_city'),
                                state=org_details.get('organization_state'),
                                country=org_details.get('organization_country'),
                                zipcode=org_details.get('organization_zipcode'),
                                office_phone=org_details.get('organization_office_phone'),
                                website=org_details.get('organization_website'),
                                org_id=OrganizationIdCreator().generateId()
        )
        organization._configure_organization_settings()
        return organization

    @classmethod
    def create_trial_organization(cls, org_details):
        organization = Organization(name=org_details.get('organization_name'),
                                sector=org_details.get('organization_sector'),
                                city=org_details.get('organization_city'),
                                country=org_details.get('organization_country'),
                                org_id=OrganizationIdCreator().generateId(),
                                in_trial_mode = True
        )
        organization_setting = organization._configure_organization_settings()
#        organization_setting.sms_tel_number = settings.TRIAL_ACCOUNT_PHONE_NUMBER
        return organization


    def _configure_organization_settings(self):
        organization_setting = OrganizationSetting()
        organization_setting.organization = self
        self.organization_setting = organization_setting
        organization_setting.document_store = slugify("%s_%s_%s" % ("HNI", self.name, self.org_id))
        return organization_setting

        
class DataSenderOnTrialAccount(models.Model):
    mobile_number = models.TextField(unique=True, primary_key=True)
    organization = models.ForeignKey(Organization)


class NGOUserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    title = models.TextField()
    org_id = models.TextField()
    office_phone = models.TextField(null=True, blank=True)
    mobile_phone = models.TextField(null=True, blank=True)
    skype = models.TextField(null=True)
    reporter_id = models.CharField(null=True, max_length=20)

    @property
    def reporter(self):
        return self.reporter_id is not None


class SMSC(models.Model):
    vumi_username = models.TextField()

    def __unicode__(self):
        return self.vumi_username


class OrganizationSetting(models.Model):
    organization = models.ForeignKey(Organization, unique=True)
    document_store = models.TextField()
    sms_tel_number = models.TextField(unique=True, null=True)
    smsc = models.ForeignKey(SMSC, null=True,
                             blank=True) # The SMSC could be blank or null when the organization is created and it may be assigned later.

    def __unicode__(self):
        return self.organization.name







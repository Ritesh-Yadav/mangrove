from datetime import datetime
from django.template.defaultfilters import slugify
from nose.tools import raises
from datawinners.accountmanagement.forms import LoginForm
from datawinners.accountmanagement.models import Organization, NGOUserProfile, OrgSettings, create_trial_organization
from django.contrib.auth.models import User
from mangrove.errors.MangroveException import AccountExpiredException
from datawinners.accountmanagement.organization_id_creator import OrganizationIdCreator

import unittest

class FakeUser(User):
    class Meta:
        proxy = True
    
    def __init__(self, org_id):
        self.org_id = org_id

    def get_profile(self):
        profile = NGOUserProfile()
        profile.org_id = self.org_id
        return profile

class FakeForm(LoginForm):
    def __init__(self, org_id):
        self.user_cache = FakeUser(org_id)

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.organization = create_trial_organization({'organization_name': 'organization_name',
                                                  'organization_sector': 'organization_sector',
                                                  'organization_city': 'organization_city',
                                                  'organization_country': 'organization_country'})
        self.organization.settings.active_date = datetime(2011,07,11)
        self.organization.settings.save()

    @raises(AccountExpiredException)
    def test_should_raise_a_trial_account_expired_exception_if_trial_account_is_expired(self):
        form = FakeForm(org_id = self.organization.org_id)
        form.check_trial_account_expired()

    def tearDown(self):
        self.organization.delete()

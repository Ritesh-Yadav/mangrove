from django.utils import unittest
from datawinners.accountmanagement.post_activation_events import active_organization
from datawinners.accountmanagement.models import NGOUserProfile, Organization, create_organization
from django.contrib.auth.models import User

class TestPostActivationEvents(unittest.TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(username='user_for_active@org.com',email='user_for_active@org.com',password='1')
        self.user.save()
        self.org = create_organization(dict(organization_name='test_org_for_correct_active_date', organization_sector='PublicHealth',
                                            organization_address='add', organization_city='city',organization_state='foo',
                                            organization_country='country',
                                            organization_office_phone='122333444',
                                            organization_website='www.google.com',
                                            organization_zipcode='10000'))
        self.profile = NGOUserProfile(user=self.user, title='Mr.', org_id=self.org.org_id)
        self.profile.save()

    def test_active_organization_with_should_active_date_is_none_save_active_date(self):
        active_organization(org = self.org)
        self.assertIsNotNone(Organization.objects.get(org_id=self.org.org_id).settings.active_date)
        self.assertEqual(Organization.objects.get(org_id=self.org.org_id).settings.active_date.microsecond,0)

    def tearDown(self):
        self.profile.delete()
        self.org.delete()
        self.user.delete()

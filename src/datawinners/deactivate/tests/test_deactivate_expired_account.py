from datetime import datetime, timedelta
import dircache
import os
from django.conf import settings
from django.contrib.auth.models import User
from datawinners.accountmanagement.models import NGOUserProfile, create_organization, create_trial_organization, Organization
from datawinners.deactivate.deactive import get_creator, get_expired_trial_organizations_without_deactivate_email_sent, create_email, get_creators, send_deactivate_email


import unittest

class TestDeactivateExpiredAccount(unittest.TestCase):

    def prepare_organization(self):
        self.expired_organization_out_of_31_days = create_trial_organization({'organization_name':'test_org_for_expired_organization_out_of_31_days',
                                                                              'organization_sector':'PublicHealth',
                                                                              'organization_city': 'xian',
                                                                              'organization_country': 'china',
                                                                              })
        self.expired_organization_out_of_31_days.settings.active_date = datetime.today() - timedelta(days=31)

        self.paid_organization = create_organization(dict(organization_name='test_org_for_paid_account',
                                              organization_sector='PublicHealth', organization_address='add',
                                              organization_city='xian', organization_country='china',organization_state='china',
                                              organization_office_phone='12233',organization_zipcode='10000', organization_website='dsdsdsdsd'))
        self.paid_organization.settings.active_date = datetime(2011, 8, 15)

        self.unexpired_organization = create_trial_organization(dict(organization_name='test_org_for_unexpired_account',
                                                   organization_sector='PublicHealth', organization_address='add',
                                                   organization_city='xian', organization_country='china',
                                                   organization_zipcode='10000'))
        self.unexpired_organization.settings.active_date = datetime.today()

        self.expired_organization_of_30_days = create_trial_organization(dict(organization_name='test_org_for_expired_organization_of_30_days',
                                                            organization_sector='PublicHealth', organization_address='add',
                                                            organization_city='xian', organization_country='china',
                                                            organization_zipcode='10000'))
        self.expired_organization_of_30_days.settings.active_date = datetime.today() - timedelta(days=30)

        self.expired_organization_of_30_days.save()
        self.expired_organization_out_of_31_days.save()
        self.unexpired_organization.save()
        self.paid_organization.save()

    def setUp(self):
        self.user1 = User(username='expired1@mail.com', email= 'expired1@mail.com', password='expired',first_name='first_name1',last_name='last_name1')
        self.user2 = User(username='expired2@mail.com', email= 'expired2@mail.com', password='expired',first_name='first_name2',last_name='last_name2')
        self.user1.set_password('expired')
        self.user2.set_password('expired')
        self.user1.save()
        self.user2.save()

        self.prepare_organization()

        NGOUserProfile(user = self.user1,title = 'Mr.',org_id = self.expired_organization_of_30_days.org_id).save()
        NGOUserProfile(user = self.user2,title = 'Ms.',org_id = self.expired_organization_of_30_days.org_id).save()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.expired_organization_of_30_days.delete()
        self.expired_organization_out_of_31_days.delete()
        self.unexpired_organization.delete()
        self.paid_organization.delete()

    def test_get_organization_creator_should_return_first_user_of_organization(self):
        self.assertEqual(get_creator(self.expired_organization_of_30_days),self.user1)

#    def test_should_not_contain_unexpired_organizations(self):
#        organizations = get_expired_trial_organizations_without_deactivate_email_sent()
#        self.assertIn(self.expired_organization_of_30_days,organizations)
#        self.assertNotIn(self.unexpired_organization,organizations)

    def test_should_not_contain_paid_organizations(self):
        organizations = get_expired_trial_organizations_without_deactivate_email_sent()
        self.assertNotIn(self.paid_organization, organizations)

#    def test_should_not_contain_organization_active_date_out_of_31_days(self):
#        organizations = get_expired_trial_organizations_without_deactivate_email_sent()
#        self.assertIn(self.expired_organization_out_of_31_days, organizations)

    def test_get_user_list_should_return_organization_creator(self):
        creators = get_creators([self.expired_organization_of_30_days])
        self.assertIn(self.user1, creators)

    def test_create_email_should_get_email_with_html_content(self):
        msg1 = create_email(self.user1)
        msg2 = create_email(self.user2)
        self.assertEqual(msg1.content_subtype,'html')
        self.assertEqual(msg2.content_subtype,'html')

    def test_create_email_should_get_email_with_right_subject(self):
        msg1 = create_email(self.user1)
        msg2 = create_email(self.user2)
        self.assertEqual(msg1.subject,'Account Expired')
        self.assertEqual(msg2.subject,'Account Expired')

    def test_create_email_should_get_email_contain_right_user_name(self):
        msg1 = create_email(self.user1)
        msg2 = create_email(self.user2)
        self.assertIn(self.user1.first_name+' '+self.user1.last_name ,msg1.body)
        self.assertIn(self.user2.first_name+' '+self.user2.last_name ,msg2.body)

    def test_create_email_should_get_right_recipient(self):
        msg1 = create_email(self.user1)
        msg2 = create_email(self.user2)
        self.assertIn(self.user1.email,msg1.to)
        self.assertIn(self.user2.email,msg2.to)
#
#    def test_deactivate_email_sent(self):
#        settings.EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#        settings.EMAIL_FILE_PATH = 'email'
#        print Organization.objects.filter(settings__in_trial_mode=True)
#        send_deactivate_email()
#        list = dircache.listdir('email')
#        print list
#        emails = ''
#        for email in list:
#            emails += open('email/'+email, 'r').read()
#            os.remove('email/'+email)
#        self.assertIn('From: ' + settings.EMAIL_HOST_USER, emails)
#        self.assertIn('To: chinatwu@gmail.com', emails)
#        self.assertIn('Subject: Account Expired', emails)

    def test_deactivate_email_only_sent_once(self):
        print Organization.objects.all()
        organisation_list = get_expired_trial_organizations_without_deactivate_email_sent()
        number_before = len(organisation_list)
        self.assertIsNot(0, number_before)

        send_deactivate_email()
        organisation_list = get_expired_trial_organizations_without_deactivate_email_sent()
        number_after = len(organisation_list)
        self.assertLess(number_after, number_before)
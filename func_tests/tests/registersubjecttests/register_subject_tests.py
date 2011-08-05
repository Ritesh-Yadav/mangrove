# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.registersubjectpage.register_subject_page import RegisterSubjectPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_ADD_SUBJECT
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.registersubjecttests.register_subject_data import *


class TestRegisterSubject(BaseTest):

    def prerequisites_of_register_subject(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.driver.go_to(DATA_WINNER_ADD_SUBJECT)
        return RegisterSubjectPage(self.driver)

    @attr('functional_test', 'smoke')
    def test_successful_registration_of_subject(self):
        """
        Function to test the successful registration of subject with given
        details
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.successfully_register_subject_with(VALID_DATA)
        self.assertRegexpMatches(register_subject_page.get_flash_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_with_existing_data(self):
        """
        Function to test the registration of subject with existing short code
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.register_subject_with(EXISTING_SHORT_CODE)
        self.assertEqual(register_subject_page.get_error_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_with_auto_generate_false(self):
        """
        Function to test the registration of subject with auto generate false
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.successfully_register_subject_with(AUTO_GENERATE_FALSE)
        self.assertRegexpMatches(register_subject_page.get_flash_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_without_location_name(self):
        """
        Function to test the registration of subject without location name
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.successfully_register_subject_with(WITHOUT_LOCATION_NAME)
        self.assertRegexpMatches(register_subject_page.get_flash_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_without_gps(self):
        """
        Function to test the registration of subject without GPS
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.successfully_register_subject_with(WITHOUT_GPS)
        self.assertRegexpMatches(register_subject_page.get_flash_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_invalid_latitude_gps(self):
        """
        Function to test the registration of subject with invalid latitude
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.register_subject_with(INVALID_LATITUDE_GPS)
        self.assertEqual(register_subject_page.get_error_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_invalid_longitude_gps(self):
        """
        Function to test the registration of subject with invalid latitude
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.register_subject_with(INVALID_LONGITUDE_GPS)
        self.assertEqual(register_subject_page.get_error_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_invalid_gps(self):
        """
        Function to test the registration of subject with invalid gps
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.register_subject_with(INVALID_GPS)
        self.assertEqual(register_subject_page.get_error_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_invalid_gps_with_comma(self):
        """
        Function to test the registration of subject with invalid gps with comma
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.register_subject_with(INVALID_GPS_WITH_COMMA)
        self.assertEqual(register_subject_page.get_error_message(), message)

    @attr('functional_test')
    def test_registration_of_subject_with_unicode_in_gps(self):
        """
        Function to test the registration of subject with unicode in GPS
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.register_subject_with(WITH_UNICODE_IN_GPS)
        self.assertEqual(register_subject_page.get_error_message(), message)

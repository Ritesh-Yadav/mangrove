# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import time
from nose.plugins.attrib import attr
from unittest.case import SkipTest

from framework.base_test import BaseTest
from framework.utils.common_utils import CommonUtilities
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.registerreporterpage.register_reporter_page import ReporterRegistrationPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_CREATE_DATA_SENDERS
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.registerreportertests.register_reporter_data import *


class TestRegisterReporter(BaseTest):

    def prerequisites_of_register_reporter(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.do_successful_login_with(VALID_CREDENTIALS)

        # doing reporter registration
        self.driver.go_to(DATA_WINNER_CREATE_DATA_SENDERS)
        return ReporterRegistrationPage(self.driver)

    @attr('functional_test', 'smoke')
    def test_successful_registration_of_reporter(self):
        """
        Function to test the successful registration of reporter with given
        details e.g. first name, last name, telephone number and commune
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(VALID_DATA)
        self.assertRegexpMatches(register_reporter_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(VALID_DATA)))

    @attr('functional_test')
    def test_registration_of_reporter_without_entering_data(self):
        """
        Function to test the registration of reporter without giving any data
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(BLANK_FIELDS)
        time.sleep(5)
        self.assertEqual(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(BLANK_FIELDS)))

    @attr('functional_test')
    def test_registration_of_reporter_with_existing_data(self):
        """
        Function to test the registration of reporter with given existing
        details e.g. first name, last name, telephone number and commune
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(EXISTING_DATA)
        time.sleep(5)
        self.assertEqual(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(EXISTING_DATA)))

    @attr('functional_test')
    def test_registration_of_reporter_without_location_name(self):
        """
        Function to test the registration of reporter without giving location name
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(WITHOUT_LOCATION_NAME)
        self.assertRegexpMatches(register_reporter_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(WITHOUT_LOCATION_NAME)))

    @attr('functional_test')
    def test_registration_of_reporter_without_gps(self):
        """
        Function to test the registration of reporter with invalid GPS
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(WITHOUT_GPS)
        self.assertRegexpMatches(register_reporter_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(WITHOUT_GPS)))

    @attr('functional_test')
    def test_registration_of_reporter_with_invalid_gps(self):
        """
        Function to test the registration of reporter with invalid GPS
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(INVALID_GPS)
        self.assertRegexpMatches(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(INVALID_GPS)))

    @attr('functional_test')
    def test_registration_of_reporter_with_invalid_latitude_gps(self):
        """
        Function to test the registration of reporter with invalid GPS
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(INVALID_LATITUDE_GPS)
        self.assertRegexpMatches(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(INVALID_LATITUDE_GPS)))

    @attr('functional_test')
    def test_registration_of_reporter_with_invalid_longitude_gps(self):
        """
        Function to test the registration of reporter with invalid GPS
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(INVALID_LONGITUDE_GPS)
        self.assertRegexpMatches(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(INVALID_LONGITUDE_GPS)))

    @attr('functional_test')
    def test_registration_of_reporter_with_unicode_in_gps(self):
        """
        Function to test the registration of reporter with invalid GPS
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(WITH_UNICODE_IN_GPS)
        self.assertRegexpMatches(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(WITH_UNICODE_IN_GPS)))

    @attr('functional_test')
    def test_registration_of_reporter_with_invalid_gps_with_comma(self):
        """
        Function to test the registration of reporter with invalid GPS
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(INVALID_GPS_WITH_COMMA)
        self.assertRegexpMatches(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(INVALID_GPS_WITH_COMMA)))

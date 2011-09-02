# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import time
from nose.plugins.attrib import attr

from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.adddatasenderspage.add_data_senders_page import AddDataSenderPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_CREATE_DATA_SENDERS
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.adddatasenderstests.add_data_senders_data import *


class TestAddDataSender(BaseTest):
    def prerequisites_of_add_data_sender(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.do_successful_login_with(VALID_CREDENTIALS)

        # doing Addition of DataSender
        self.driver.go_to(DATA_WINNER_CREATE_DATA_SENDERS)
        return AddDataSenderPage(self.driver)

    @attr('functional_test', 'smoke')
    def test_successful_addition_of_data_sender(self):
        """
        Function to test the successful Addition of DataSender with given
        details e.g. first name, last name, telephone number and commune
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(VALID_DATA)
        self.assertRegexpMatches(add_data_sender_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(VALID_DATA)))

    @attr('functional_test')
    def test_addition_of_data_sender_without_entering_data(self):
        """
        Function to test the Addition of DataSender without giving any data
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(BLANK_FIELDS)
        time.sleep(5)
        self.assertEqual(add_data_sender_page.get_error_message(),
                         fetch_(ERROR_MSG, from_(BLANK_FIELDS)))

    @attr('functional_test')
    def test_addition_of_data_sender_with_existing_data(self):
        """
        Function to test the Addition of DataSender with given existing
        details e.g. first name, last name, telephone number and commune
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(EXISTING_DATA)
        time.sleep(5)
        self.assertEqual(add_data_sender_page.get_error_message(),
                         fetch_(ERROR_MSG, from_(EXISTING_DATA)))

    @attr('functional_test')
    def test_addition_of_data_sender_without_location_name(self):
        """
        Function to test the Addition of DataSender without giving location name
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(WITHOUT_LOCATION_NAME)
        self.assertRegexpMatches(add_data_sender_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(WITHOUT_LOCATION_NAME)))

    @attr('functional_test')
    def test_addition_of_data_sender_without_gps(self):
        """
        Function to test the Addition of DataSender with invalid GPS
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(WITHOUT_GPS)
        self.assertRegexpMatches(add_data_sender_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(WITHOUT_GPS)))

    @attr('functional_test')
    def test_addition_of_data_sender_with_invalid_gps(self):
        """
        Function to test the Addition of DataSender with invalid GPS
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(INVALID_GPS)
        self.assertEqual(add_data_sender_page.get_error_message(),
                         fetch_(ERROR_MSG, from_(INVALID_GPS)))

    @attr('functional_test')
    def test_addition_of_data_sender_with_invalid_latitude_gps(self):
        """
        Function to test the Addition of DataSender with invalid GPS
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(INVALID_LATITUDE_GPS)
        self.assertEqual(add_data_sender_page.get_error_message(),
                         fetch_(ERROR_MSG, from_(INVALID_LATITUDE_GPS)))

    @attr('functional_test')
    def test_addition_of_data_sender_with_invalid_longitude_gps(self):
        """
        Function to test the Addition of DataSender with invalid GPS
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(INVALID_LONGITUDE_GPS)
        self.assertEqual(add_data_sender_page.get_error_message(),
                         fetch_(ERROR_MSG, from_(INVALID_LONGITUDE_GPS)))

    @attr('functional_test')
    def test_addition_of_data_sender_with_unicode_in_gps(self):
        """
        Function to test the Addition of DataSender with invalid GPS
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(WITH_UNICODE_IN_GPS)
        self.assertEqual(add_data_sender_page.get_error_message(),
                         fetch_(ERROR_MSG, from_(WITH_UNICODE_IN_GPS)))

    @attr('functional_test')
    def test_addition_of_data_sender_with_invalid_gps_with_comma(self):
        """
        Function to test the Addition of DataSender with invalid GPS
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(INVALID_GPS_WITH_COMMA)
        self.assertEqual(add_data_sender_page.get_error_message(),
                         fetch_(ERROR_MSG, from_(INVALID_GPS_WITH_COMMA)))

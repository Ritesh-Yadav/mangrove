# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import time
import unittest
from nose.plugins.attrib import attr

from framework.base_test import BaseTest, setup_driver, teardown_driver
from framework.utils.database_manager_postgres import DatabaseManager
from pages.registrationpage.registration_page import RegistrationPage
from registration_data import *
from testdata.test_data import DATA_WINNER_REGISTER_PAGE

def register_and_get_email(driver):
    driver.go_to(DATA_WINNER_REGISTER_PAGE)
    registration_page = RegistrationPage(driver)
    return registration_page.successful_registration_with(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)

class TestRegistrationPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = setup_driver()

    @classmethod
    def tearDownClass(cls):
        teardown_driver(cls.driver)
        
    @attr('functional_test', 'smoke')
    def test_successful_registration(self):
        registration_confirmation_page, email = register_and_get_email(self.driver)
        self.assertEquals(registration_confirmation_page.registration_success_message(), REGISTRATION_SUCCESS_MESSAGE)
        dbmanager = DatabaseManager()
        dbmanager.delete_organization_all_details(email)

    @attr('functional_test')
    def test_register_ngo_with_existing_email_address(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(EXISTING_EMAIL_ADDRESS)
        self.assertEquals(registration_page.get_error_message(), EXISTING_EMAIL_ADDRESS_ERROR_MESSAGE)

    @attr('functional_test')
    def test_register_ngo_with_unmatched_passwords(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(UNMATCHED_PASSWORD)
        self.assertEquals(registration_page.get_error_message(),UNMATCHED_PASSWORD_ERROR_MESSAGE)

    @attr('functional_test')
    def test_register_ngo_without_entering_data(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(WITHOUT_ENTERING_REQUIRED_FIELDS)
        self.assertEquals(registration_page.get_error_message(),WITHOUT_ENTERING_REQUIRED_FIELDS_ERROR_MESSAGE)

    @attr('functional_test')
    def test_register_ngo_with_invalid_web_url(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(INVALID_WEBSITE_URL)
        self.assertEquals(registration_page.get_error_message(),INVALID_WEBSITE_URL_ERROR_MESSAGE)


# vim: ai ts=4 sts=4 et sw=4utf-8
from nose.plugins.attrib import attr
from framework.base_test import BaseTest
from framework.utils.data_fetcher import from_, fetch_
from pages import page
from pages.loginpage.login_page import LoginPage
from pages.page import Page
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import *


class ExpiredTrailPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_error_message(self):
     """
     Function to fetch the error messages from error label of the login
     page

     Return error message
     """
     error_message = ""
     locators = self.driver.find_elements_(ERROR_MESSAGE_LABEL)
     if locators:
         for locator in locators:
             error_message = error_message + locator.text
     return error_message.replace("\n", " ")


class TestLoginPage(BaseTest):
    @attr('functional_test', 'smoke')
    def test_login_with_valid_credentials(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.assertEqual(dashboard_page.welcome_message(),
                         fetch_(WELCOME_MESSAGE, from_(VALID_CREDENTIALS)))

    @attr('functional_test')
    def test_login_with_unactivated_account_credentials(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(UNACTIVATED_ACCOUNT_CREDENTIALS)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE,
                                from_(UNACTIVATED_ACCOUNT_CREDENTIALS)))

    @attr('functional_test')
    def test_login_with_invalid_format_email_address(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_EMAIL_ID_FORMAT)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(INVALID_EMAIL_ID_FORMAT)))

    @attr('functional_test')
    def test_login_with_invalid_password_credential(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_PASSWORD)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(INVALID_PASSWORD)))

    @attr('functional_test')
    def test_login_without_entering_email_address(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_EMAIL_ADDRESS)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(BLANK_EMAIL_ADDRESS)))

    @attr('functional_test')
    def test_login_without_entering_password(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_PASSWORD)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(BLANK_PASSWORD)))

    @attr('functional_test')
    def test_login_without_entering_email_and_password(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_CREDENTIALS)
        self.assertEqual(login_page.get_error_message(), fetch_(ERROR_MESSAGE,
                                                                from_(BLANK_CREDENTIALS)))

    @attr('functional_test')
    def test_register_link_functionality(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        register_page = login_page.navigate_to_registration_page()
        self.assertEqual(self.driver.get_title(), "Register")

    @attr('functional_test')
    def test_login_with_expired_trial_account(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)

        login_page = LoginPage(self.driver)
        login_page.login_with(EXPIRED_TRAIL_ACCOUNT)

        expired_trail_account_page = ExpiredTrailPage(self.driver)

        self.assertEqual(expired_trail_account_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(EXPIRED_TRAIL_ACCOUNT)))



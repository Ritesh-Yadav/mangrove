
from framework.base_test import BaseTest
from framework.mangrovetests.login_page import LoginPage
from nose.tools import *
import time

__author__ = 'kumarr'


class TestLoginPage(BaseTest):

    def test_login_with_valid_credentials(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        dashboard_page= login_page.successful_login("nogo@mail.com", "nogo123")
        eq_(dashboard_page.welcome_message(), "Welcome Mr. No Go",
          "Login Un-successful or UserName is not Present")


    def test_login_with_invalid_email_address(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.enter_credentials_and_submit("invalid@mail", "nogo123")
        time.sleep(5)
        print self.driver.get_page_source()
        eq_(login_page.get_error_message(),
                         "Your username and password didn't match. Please try again")

    def test_login_with_invalid_password_credential(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.enter_credentials_and_submit("invalid@mail.com", "nogo123")
        eq_(login_page.get_error_message(),
                         "Your username and password didn't match. Please try again")


    def test_login_without_entering_email_address(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.enter_credentials_and_submit("", "nogo123")
        eq_(login_page.get_error_message(),
                         "Your username and password didn't match. Please try again")


    def test_login_without_entering_password(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.enter_credentials_and_submit("nogo@mail.com", "")
        eq_(login_page.get_error_message(),
                         "Your username and password didn't match. Please try again")

    def test_login_without_entering_email_and_password(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.enter_credentials_and_submit("","")
        eq_(login_page.get_error_message(),
                         "Your username and password didn't match. Please try again")

    def test_register_link_functionality(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        register_page=login_page.navigate_to_registration_page()
        eq_(register_page.get_title(), "Register", "Registration Page Title is incorrect or Register Link is Not Working")

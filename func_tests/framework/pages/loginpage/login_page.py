# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from selenium.webdriver.common.by import By

from framework.pages.page import Page
from framework.pages.dashboardpage.dashboard_page import DashboardPage
from framework.pages.registrationpage.registration_page import  RegistrationPage
from framework.utils.common_utils import CommonUtilities
from framework.utils.data_fetcher import *
from framework.pages.loginpage.login_locator import *
from tests.logintests.login_data import *


class LoginPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def login_with(self, login_credential):
        """
        Function to login into the website with valid credentials

        Args:
        'email_id' is registered email id of the user
        'password' is the associated password with the email address

        Return DashboardPage on successful login
        """
        self.driver.find_text_box(EMAIL_TB).enter_text(fetch_(USERNAME, from_(login_credential)))
        self.driver.find_text_box(PASSWORD_TB).enter_text(fetch_(PASSWORD,from_(login_credential)))
        self.driver.find(LOGIN_BTN).click()
        return self

    def for_successful_login(self, email_id, password):
        """
        Function to login into the website with valid credentials

        Args:
        'email_id' is registered email id of the user
        'password' is the associated password with the email address

        Return DashboardPage on successful login
        """
        self.driver.find_text_box(EMAIL_TB).send_keys(email_id)
        self.driver.find_text_box("password").enter_text(password)
        self.driver.find_element_by_css_selector("input[value='Login']").click()
        return DashboardPage(self.driver)

    def enter_credentials_and_submit(self, email_id, password):
        """
        Function to enter email id and password in the text boxes and click
        on the login button. This function is used for testing error messages
         only
         .
        Args:
        'email_id' is registered email id of the user
        'password' is the associated password with the email address

        Return LoginPage 
        """
        self.driver.find_text_box("username").enter_text(email_id)
        self.driver.find_text_box("password").enter_text(password)
        self.driver.find_element_by_css_selector("input[value='Login']").click()
        return self

    def get_error_message(self):
        """
        Function to fetch the error messages from error label of the login
        page

        Return error message
        """
        error_message = ""
        locator1 = CommonUtilities(self.driver).is_element_present \
            ("//div[contains(@class,'error') and contains(@class, 'message-box')]", By.XPATH)
        if locator1:
            error_message = error_message + locator1.text
        print error_message
        return error_message

    def error_message(self):
        """
        Method to extract one error message present on Login Page:

        Returns error messages
        """

        error_message = self.driver.find(ERROR_MESSAGE_LI).text
        return error_message
    
    def error_messages(self):
        """
        Method to extract all error messages present on Login Page:
        
        Returns error messages   
        """
        error_messages = self.driver.find_element_by_class_name("errorlist").find_elements_by_tag_name("li")
        print error_messages
        for eachError in error_messages:
            print eachError.text
            return [ eachError.text for eachError in error_messages ]
    
    

    def navigate_to_registration_page(self):
        """
        Function to click on register page link which is available on the login page

        Return RegistrationPage
        """
        self.driver.find_element_by_css_selector("a[href='/register']").click()
        return RegistrationPage(self.driver)

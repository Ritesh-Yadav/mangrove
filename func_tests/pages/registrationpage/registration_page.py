# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import generateId

from pages.page import Page
from pages.registerconfirmationpage.registration_confirmation_page import RegistrationConfirmationPage
from framework.utils.data_fetcher import *
from pages.registrationpage.registration_locator import *
from tests.registrationtests.registration_data import *


class RegistrationPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def successful_registration_with(self, registration_data):
        registration_data = dict(registration_data) # create a copy so we don't modify in place
        email = registration_data[EMAIL] + generateId() + "@ngo.com"
        registration_data[EMAIL] = email
        self.register_with(registration_data)
        return RegistrationConfirmationPage(self.driver), email

    def register_with(self, registration_data):
        self.driver.find(AGREE_TERMS_CB).click()
        for key,value in registration_data.items():
            if key in [ORGANIZATION_SECTOR]:
                self.driver.find_drop_down(by_css("select[name=%s]" % key)).set_selected(value)
            elif key in [PAY_MONTHLY, WIRE_TRANSFER]:
                self.driver.find_radio_button(by_css("input[value=%s]" % key)).click()
            else:
                self.driver.find_text_box(by_css("input[name=%s]" % key)).enter_text(value)

        self.driver.find(ORGANIZATION_REGISTER_BTN).click()
        return self

    def get_error_message(self):
        error_message = ""
        locators = self.driver.find_elements_(ERROR_MESSAGE_LABEL)
        if locators:
            for locator in locators:
                error_message = error_message + locator.text
        return error_message.replace("\n", " ")

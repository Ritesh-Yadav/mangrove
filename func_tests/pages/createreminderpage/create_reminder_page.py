# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.reviewpage.review_page import ReviewPage
from pages.page import Page
from framework.utils.data_fetcher import *
from pages.createreminderpage.create_reminder_locator import *
from framework.utils.common_utils import *


class CreateReminderPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def save_reminder_successfully(self):
        """
        Function to save the data on set up reminder page

        Return ReviewPage
        """
        self.driver.find(SAVE_CHANGES_BTN).click()
        return ReviewPage(self.driver)

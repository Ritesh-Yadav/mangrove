# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.data_fetcher import *
from pages.adddatasenderspage.add_data_senders_page import AddDataSenderPage
from pages.alldatasenderspage.all_data_senders_locator import *
from pages.page import Page
from tests.alldatasendertests.all_data_sender_data import *


class AllDataSendersPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_add_a_data_sender_page(self):
        """
        Function to navigate to add a data sender page of the website

        Return create project page
         """
        self.driver.find(ADD_A_DATA_SENDER_LINK).click()
        return AddDataSenderPage(self.driver)

    def select_a_data_sender_by_mobile(self, data_sender_mobile):
        """
        Function to select a data sender on all data sender page

        Return self
         """
        self.driver.find(ADD_A_DATA_SENDER_LINK).click()
        return AddDataSenderPage(self.driver)

    def select_a_data_sender_by_id(self, data_sender_id):
        """
        Function to select a data sender on all data sender page

        Return self
         """
        mobile_number = fetch_(MOBILE_NUMBER)
        self.driver.find(ADD_A_DATA_SENDER_LINK).click()
        return AddDataSenderPage(self.driver)

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
         """
        self.driver.find(by_xpath(DATA_SENDER_CHECK_BOX_BY_MOBILE_XPATH % data_sender_mobile)).click()

    def select_a_data_sender_by_id(self, data_sender_id):
        """
        Function to select a data sender on all data sender page
         """
        self.driver.find(by_xpath(DATA_SENDER_CHECK_BOX_BY_UID_XPATH % data_sender_id)).click()

    def select_project(self, project_name):
        """
        Function to select a project on all data sender page
         """
        self.driver.find(by_xpath(PROJECT_CB_XPATH % project_name)).click()

    def select_projects(self, project_names):
        """
        Function to select multiple projects on all data sender page

        Args:
        project_names is list of all the projects

         """
        for project_name in project_names:
            self.select_project(project_name)

    def click_confirm(self, wait=False):
        """
        Function to confirm the association/dissociation with projects on all data sender page
         """
        self.driver.find(CONFIRM_BUTTON).click()
        if wait:
            self.driver.wait_until_modal_dismissed(7)

    def click_cancel(self):
        """
        Function to cancel the association/dissociation with projects on all data sender page
         """
        self.driver.find(CANCEL_LINK).click()

    def associate_data_sender(self):
        """
        Function to associate data sender with project
         """
        self.driver.find_drop_down(ACTION_DROP_DOWN).set_selected(ASSOCIATE)

    def dissociate_data_sender(self):
        """
        Function to dissociate data sender with project
         """
        self.driver.find_drop_down(ACTION_DROP_DOWN).set_selected(DISSOCIATE)

    def get_success_message(self):
        """
        Function to fetch the success message from success label
         """
        return self.driver.find(SUCCESS_MESSAGE_LABEL).text

    def get_error_message(self):
        """
        Function to fetch the error message from success label
         """
        return self.driver.find(ERROR_MESSAGE_LABEL).text

    def get_project_names(self, data_sender_id):
        """
        Function to fetch the associated project names from the all data senders page
         """
        return self.driver.find(by_xpath(PROJECT_NAME_LABEL_XPATH % data_sender_id)).text

    def get_uid(self, data_sender_mobile):
        """
        Function to fetch the mobile number from the all data senders page
         """
        return self.driver.find(by_xpath(UID_LABEL_BY_MOBILE_XPATH % data_sender_mobile)).text

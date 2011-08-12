# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import CommonUtilities, generateId
from pages.page import Page
from pages.createdatasenderquestionnairepage.create_data_sender_questionnaire_locator import *
from framework.utils.common_utils import *
from pages.reviewandtestpage.review_and_test_page import ReviewAndTestPage


class CreateDataSenderQuestionnairePage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def successfully_create_data_sender_questionnaire_with(self, subject_data):
        """
        Function to enter and save the data on set up project page

        Args:
        registration_data is data to fill in the different fields like first
        name, last name, telephone number and commune

        Return self
        """
        self.driver.find(SAVE_CHANGES_BTN).click()
        return ReviewAndTestPage(self.driver)

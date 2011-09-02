# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.createreminderpage.create_reminder_page import CreateReminderPage
from pages.page import Page
from pages.createdatasenderquestionnairepage.create_data_sender_questionnaire_locator import *


class CreateDataSenderQuestionnairePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def save_questionnnaire_successfully(self):
        """
        Function to save the data sender questionnaire

        Return CreateReminderPage
        """
        self.driver.find(SAVE_CHANGES_BTN).click()
        return CreateReminderPage(self.driver)

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.utils.common_utils import generateId
from pages.page import Page
from framework.utils.data_fetcher import from_, fetch_
from pages.addsubjecttypepage.add_subject_type_locator import *
from tests.addsubjecttypetests.add_subject_type_data import *


class AddSubjectTypePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def successfully_add_entity_type_with(self, entity_data):
        """
        Function to enter randomly generated entity type in the text box and click on the Add button
         .
        Args:
        'entity_data' is entity name

        Return self
        """
        entity_type = fetch_(ENTITY_TYPE, from_(entity_data)) + generateId()
        self.driver.find_text_box(NEW_SUBJECT_TB).enter_text(entity_type)
        self.driver.find(ADD_BTN).click()
        self.driver.wait_until_element_is_not_present(5, by_css("#type_message .ajax_loader"))
        return entity_type

    def add_entity_type_with(self, entity_data):
        """
        Function to enter entity type in the text box and click on the Add button
         .
        Args:
        'entity_data' is entity name

        Return self
        """
        self.driver.find_text_box(NEW_SUBJECT_TB).enter_text(fetch_(ENTITY_TYPE, from_(entity_data)))
        self.driver.find(ADD_BTN).click()
        return self

    def get_error_message(self):
        """
        Function to fetch the error message from error label of the Add a new subject type
        page

        Return error message
        """
        return self.driver.find(ERROR_MESSAGE_LABEL).text

    def click_on_accordian_link(self):
        """
        Function to open/close the accordian of the add a subject type

        Return self
        """
        self.driver.find(ADD_NEW_SUBJECT_TYPE_LINK).click()
        return self

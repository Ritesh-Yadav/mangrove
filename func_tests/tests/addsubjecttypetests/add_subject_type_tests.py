# vim: ai ts=4 sts=4 et sw=4utf-8
from nose.plugins.attrib import attr
import time
from framework.base_test import BaseTest
from framework.utils.data_fetcher import from_, fetch_
from pages.addsubjecttypepage.add_subject_type_page import AddSubjectTypePage
from pages.loginpage.login_page import LoginPage
from nose.plugins.skip import SkipTest
from pages.registersubjectpage.register_subject_page import RegisterSubjectPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_ADD_SUBJECT
from tests.addsubjecttypetests.add_subject_type_data import *
from tests.logintests.login_data import VALID_CREDENTIALS


class TestAddSubjectType(BaseTest):

    def prerequisites_of_add_subject_type(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.driver.go_to(DATA_WINNER_ADD_SUBJECT)
        return AddSubjectTypePage(self.driver)

    @attr('functional_test', 'smoke')
    def test_add_new_subject_type(self):
        add_subject_type_page = self.prerequisites_of_add_subject_type()
        add_subject_type_page.click_on_accordian_link()
        entity_type = add_subject_type_page.successfully_add_entity_type_with(VALID_ENTITY)
        time.sleep(2)
        add_subject_page = RegisterSubjectPage(self.driver)
        self.assertEqual(add_subject_page.get_selected_subject(), entity_type.lower())

    @attr('functional_test')
    def test_add_existing_subject_type(self):
        add_subject_type_page = self.prerequisites_of_add_subject_type()
        add_subject_type_page.click_on_accordian_link()
        add_subject_type_page.add_entity_type_with(ALREADY_EXIST_ENTITY)
        self.assertEqual(add_subject_type_page.get_error_message(), fetch_(ERROR_MESSAGE, from_(ALREADY_EXIST_ENTITY)))

    @attr('functional_test')
    def test_add_blank_subject_type(self):
        add_subject_type_page = self.prerequisites_of_add_subject_type()
        add_subject_type_page.click_on_accordian_link()
        add_subject_type_page.add_entity_type_with(BLANK)
        self.assertEqual(add_subject_type_page.get_error_message(), fetch_(ERROR_MESSAGE, from_(BLANK)))

    @attr('functional_test')
    def test_add_invalid_subject_type(self):
        add_subject_type_page = self.prerequisites_of_add_subject_type()
        add_subject_type_page.click_on_accordian_link()
        add_subject_type_page.add_entity_type_with(INVALID_ENTITY)
        self.assertEqual(add_subject_type_page.get_error_message(), fetch_(ERROR_MESSAGE, from_(INVALID_ENTITY)))

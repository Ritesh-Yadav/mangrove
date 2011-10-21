# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from nose.tools import nottest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.smstesterlightboxtests.sms_tester_light_box_data import *


class TestSMSTesterLightBox(BaseTest):

    @nottest
    def prerequisites_of_sms_tester_light_box1(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(VALID_CREDENTIALS)

        # going on all project page
        all_project_page = global_navigation.navigate_to_view_all_project_page()
        project_overview_page = all_project_page.navigate_to_project_overview_page(
            fetch_(PROJECT_NAME, from_(PROJECT_DATA)))
        edit_project_page = project_overview_page.navigate_to_edit_project_page()
        subject_questionnaire_page = edit_project_page.save_project_successfully()
        questionnaire_page = subject_questionnaire_page.save_questionnaire_successfully()
        datsender_questionnaire_page = questionnaire_page.save_questionnaire_successfully()
        reminder_page = datsender_questionnaire_page.save_questionnnaire_successfully()
        review_page = reminder_page.save_reminder_successfully()
        return review_page.open_sms_tester_light_box()

    @nottest
    def prerequisites_of_sms_tester_light_box2(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(VALID_CREDENTIALS)

        # going on all project page
        all_project_page = global_navigation.navigate_to_view_all_project_page()
        project_overview_page = all_project_page.navigate_to_project_overview_page(
            fetch_(PROJECT_NAME, from_(PROJECT_DATA)))
        return project_overview_page.open_sms_tester_light_box()

    @attr('functional_test', 'smoke')
    def test_successful_sms_submission(self):
        """
        Function to test the successful SMS submission
        """
        sms_tester_page = self.prerequisites_of_sms_tester_light_box1()
        sms_tester_page.send_sms_with(VALID_DATA)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(VALID_DATA)))

    @attr('functional_test')
    def test_sms_player_for_exceeding_word_length(self):
        """
        Function to test the error message on the sms submission page for exceeding word limit for word type question
        """
        sms_tester_page = self.prerequisites_of_sms_tester_light_box1()
        sms_tester_page.send_sms_with(EXCEED_NAME_LENGTH)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(EXCEED_NAME_LENGTH)))

    @attr('functional_test', 'smoke')
    def test_successful_sms_submission(self):
        """
        Function to test the successful SMS submission
        """
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page.send_sms_with(VALID_DATA2)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(VALID_DATA2)))

    def test_successful_ordered_sms_submission(self):
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page.send_sms_with(VALID_DATA3)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(VALID_DATA2)))

    @attr('functional_test')
    def test_sms_submission_for_unicode(self):
        """
        Function to test the SMS submission with unicodes
        """
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page.send_sms_with(SMS_WITH_UNICODE)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(SMS_WITH_UNICODE)))

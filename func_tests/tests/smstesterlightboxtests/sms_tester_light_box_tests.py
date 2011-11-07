# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from unittest.case import skipUnless, skipIf

from nose.plugins.attrib import attr
from nose.tools import nottest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.smstesterlightboxtests.sms_tester_light_box_data import *

USE_ORDERED_SMS_PARSER = False

class BasePrepare(BaseTest):
    @nottest
    def prerequisite_of_sms_test_light_box(self, project_data):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(VALID_CREDENTIALS)
        # going on all project page
        all_project_page = global_navigation.navigate_to_view_all_project_page()
        project_overview_page = all_project_page.navigate_to_project_overview_page(
            fetch_(PROJECT_NAME, from_(project_data)))
        edit_project_page = project_overview_page.navigate_to_edit_project_page()
        subject_questionnaire_page = edit_project_page.save_and_create_project_successfully()
        questionnaire_page = subject_questionnaire_page.save_questionnaire_successfully()
        datsender_questionnaire_page = questionnaire_page.save_questionnaire_successfully()
        reminder_page = datsender_questionnaire_page.save_questionnnaire_successfully()
        review_page = reminder_page.save_reminder_successfully()
        return review_page.open_sms_tester_light_box()

    @nottest
    def prerequisites_of_sms_tester_light_box1(self):

        project_data = PROJECT_DATA
        return self.prerequisite_of_sms_test_light_box(project_data)

    @nottest
    def prerequisites_of_sms_tester_light_box3(self):

        project_data = PROJECT_DATA_WITH_ACTIVITY_REPORT
        return self.prerequisite_of_sms_test_light_box(project_data)

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

@skipIf(USE_ORDERED_SMS_PARSER, "USE_ORDERED_SMS_PARSER is set, only ordered sms can be used while this is the case")
class TestSMSTesterLightBox(BasePrepare):

    @attr('functional_test', 'smoke')
    def test_successful_sms_submission(self):
        """
        Function to test the successful SMS submission
        """
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page = self.prerequisites_of_sms_tester_light_box1()
        sms_tester_page.send_sms_with(VALID_DATA)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(VALID_DATA)))

    @attr('functional_test')
    def test_sms_player_for_exceeding_word_length(self):
        """
        Function to test the error message on the sms submission page for exceeding word limit for word type question
        """
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page = self.prerequisites_of_sms_tester_light_box1()
        sms_tester_page.send_sms_with(EXCEED_NAME_LENGTH)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(EXCEED_NAME_LENGTH)))

    @attr('functional_test', 'smoke')
    def test_successful_sms_submission(self):
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page.send_sms_with(VALID_DATA2)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(VALID_DATA2)))

    @attr('functional_test', 'smoke')
    def test_sms_submission_for_unicode(self):
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page.send_sms_with(SMS_WITH_UNICODE)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(SMS_WITH_UNICODE)))

@skipUnless(USE_ORDERED_SMS_PARSER, "USE_ORDERED_SMS_PARSER is not set, only unordered sms can be used while this is the case")
class TestOrderedSMSTesterLightBox(BasePrepare):

    @attr('functional_test')
    def test_successful_ordered_sms_submission(self):
        sms_tester_page = self.prerequisites_of_sms_tester_light_box2()
        sms_tester_page.send_sms_with(VALID_ORDERED_SMS_DATA)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(VALID_ORDERED_SMS_DATA)))

    @attr('functional_test')
    def test_sms_submission_for_project_with_activity_report(self):
        sms_tester_page = self.prerequisites_of_sms_tester_light_box3()
        sms_tester_page.send_sms_with(VALID_ORDERED_SMS_DATA_WITH_ACTIVITY_REPORT)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(RESPONSE_MESSAGE, from_(VALID_ORDERED_SMS_DATA)))


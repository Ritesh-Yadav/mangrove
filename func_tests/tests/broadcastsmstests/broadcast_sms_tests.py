from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from nose.plugins.attrib import attr
from pages.loginpage.login_page import LoginPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.broadcastsmstests.broadcast_sms_data import SMS_VALID_DATA, SMS_EXACT_ON_LIMIT_DATA
from tests.editprojecttests.edit_project_data import PROJECT_NAME, ACTIVATED_PROJECT_DATA
from tests.logintests.login_data import VALID_CREDENTIALS

class TestBroadcastSMS(BaseTest):
    @attr('functional_test')
    def test_clear_sms_content_after_send(self):
        all_project_page = self.prerequisites_of_edit_project()
        project_overview_page = all_project_page.navigate_to_project_overview_page(
            fetch_(PROJECT_NAME, from_(ACTIVATED_PROJECT_DATA)))
        messages_and_reminders_page = project_overview_page.navigate_to_messages_and_reminders_page()
        messages_and_reminders_page.write_sms_content(SMS_VALID_DATA)
        messages_and_reminders_page.click_send()
        self.assertEquals(messages_and_reminders_page.get_sms_content(), "")

    @attr('functional_test')
    def test_exceed_sms_content_limitation(self):
        all_project_page = self.prerequisites_of_edit_project()
        project_overview_page = all_project_page.navigate_to_project_overview_page(
            fetch_(PROJECT_NAME, from_(ACTIVATED_PROJECT_DATA)))
        messages_and_reminders_page = project_overview_page.navigate_to_messages_and_reminders_page()
        messages_and_reminders_page.write_sms_content(SMS_EXACT_ON_LIMIT_DATA + "redundant data")
        self.assertEquals(messages_and_reminders_page.get_sms_content(), SMS_EXACT_ON_LIMIT_DATA)


    def prerequisites_of_edit_project(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(VALID_CREDENTIALS)
        return global_navigation.navigate_to_view_all_project_page()


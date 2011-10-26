from nose.plugins.attrib import attr
from framework.base_test import BaseTest
from pages.dashboardpage.dashboard_page import DashboardPage
from pages.loginpage.login_page import LoginPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.createprojecttests.create_project_data import VALID_DATA
from tests.logintests.login_data import TRIAL_CREDENTIALS
from tests.remindertests.reminder_data import WARNING_MESSAGE, REMINDER_NOT_WORK_FOR_TRIAL_MSG

class TestReminderSend(BaseTest):
    def login_with(self, account):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.do_successful_login_with(account)
        dashboard_page = DashboardPage(self.driver)
        return dashboard_page

    def create_project(self, dashboard_page):
        create_project_page = dashboard_page.navigate_to_create_project_page()
        create_project_page.create_project_with_reminder()
        return create_project_page

    def create_project_to_reminder_page(self, create_project_page):
        create_subject_questionnaire_page = create_project_page.save_project_successfully()
        create_questionnaire_page = create_subject_questionnaire_page.save_questionnaire_successfully()
        create_data_sender_questionnaire_page = create_questionnaire_page.save_questionnaire_successfully()
        reminder_page = create_data_sender_questionnaire_page.save_questionnnaire_successfully()
        return reminder_page

    def start_create_normal_project(self):
        dashboard_page = self.login_with(TRIAL_CREDENTIALS)
        create_project_page = self.create_project(dashboard_page)
        create_project_page.create_project_with(VALID_DATA)
        return create_project_page

    @attr("functional_test")
    def test_trial_account_should_see_reminder_not_work_message_when_creating_project(self):
        create_project_page = self.start_create_normal_project()
        self.create_project_to_reminder_page(create_project_page)
        message = self.driver.find(REMINDER_NOT_WORK_FOR_TRIAL_MSG).text
        self.assertEqual(WARNING_MESSAGE, message)

    def active_project_and_go_to_all_reminder_page(self, reminder_page):
        review_and_test_page = reminder_page.save_reminder_successfully()
        project_overview_page = review_and_test_page.navigate_to_project_overview_page()
        light_box = project_overview_page.open_activate_project_light_box()
        project_overview_page = light_box.activate_project()
        return project_overview_page.navigate_to_reminder_page()

    def create_reminder_for_all_week(self, reminder_page):
        for day in range(1, 8):
            reminder_page.add_new_reminder_for_days_before(day)
        reminder_page.save_reminders()


    @attr("functional_test")
    def test_trial_account_should_see_reminder_not_work_message_at_reminder_tab_in_active_project(self):
        create_project_page = self.start_create_normal_project()
        reminder_page = self.create_project_to_reminder_page(create_project_page)
        self.active_project_and_go_to_all_reminder_page(reminder_page)
        message = self.driver.find(REMINDER_NOT_WORK_FOR_TRIAL_MSG).text
        self.assertEqual(WARNING_MESSAGE, message)

    @attr("functional_test")
    def test_trial_account_should_see_reminder_not_work_message_at_sent_tab_in_active_project(self):
        create_project_page = self.start_create_normal_project()
        reminder_page = self.create_project_to_reminder_page(create_project_page)
        all_reminders_page = self.active_project_and_go_to_all_reminder_page(reminder_page)
        all_reminders_page.click_sent_reminder_tab()
        message = self.driver.find(REMINDER_NOT_WORK_FOR_TRIAL_MSG).text
        self.assertEqual(WARNING_MESSAGE, message)



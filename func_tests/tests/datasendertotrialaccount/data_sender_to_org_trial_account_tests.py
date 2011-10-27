from time import sleep
from framework.utils.data_fetcher import fetch_, from_
from framework.utils.database_manager_postgres import DatabaseManager
from pages.addsubjecttypepage.add_subject_type_page import AddSubjectTypePage
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from testdata.test_data import DATA_WINNER_SMS_TESTER_PAGE
from tests.datasendertotrialaccount.data_sender_to_org_trial_account_data import *
from tests.endtoendtest.end_to_end_tests import activate_account, do_login
from tests.registrationtests.registration_data import REGISTRATION_PASSWORD
from tests.registrationtests.trial_registration_tests import register_and_get_email_for_trial
from framework.utils.couch_http_wrapper import CouchHttpWrapper
from framework.base_test import BaseTest

# add data sender to trial account

# add data sender to paid account

# send sms to trial one
    #check sms submission in this trail display, not paid display

# send sms to paid account
    #check sms submission paid paid display, not paid display

from tests.datasendertotrialaccount.data_sender_to_org_trial_account_data import VALID_SMS_DATA_FROM_DATA_SENDER, VALID_DATA_FOR_DATA_SENDER
from tests.smstesterlightboxtests.sms_tester_light_box_data import PROJECT_NAME

class TestDataSenderAssociationWithTrialAccount(BaseTest):

    emails = []

    def add_trial_organization_and_login(driver):
        registration_confirmation_page, email = register_and_get_email_for_trial(driver)
        activate_account(driver, email)
        return do_login(driver, email, REGISTRATION_PASSWORD)

    def create_questionnaire(self, create_questionnaire_page):
        create_questionnaire_page.create_questionnaire_to_work_performed_subjects_with(QUESTIONNAIRE_DATA)
        create_data_sender_questionnaire_page = create_questionnaire_page.save_questionnaire_successfully()
        create_data_sender_questionnaire_page.save_questionnnaire_successfully().save_reminder_successfully()
        return create_data_sender_questionnaire_page

    def add_subject_type(self, valid_subject_type):
        add_subject_type_page = AddSubjectTypePage(self.driver)
        add_subject_type_page.click_on_accordian_link()
        add_subject_type_page.add_entity_type_with(valid_subject_type)

    def create_project(self, create_project_page):
        create_project_page.select_report_type(VALID_DATA_FOR_PROJECT)
        return create_project_page.create_project_with(VALID_DATA_FOR_PROJECT).save_project_successfully()

    def test_data_sender_send_SMS_to_trial_accounts_check_results(self):

        registration_confirmation_page, email = register_and_get_email_for_trial(self.driver)
        self.emails.append(email)
        activate_account(self.driver, email)
        global_navigation = do_login(self.driver, email, REGISTRATION_PASSWORD)

        dashboard_page = global_navigation.navigate_to_dashboard_page()
        self.create_questionnaire(
        self.create_project(dashboard_page.navigate_to_create_project_page()).save_questionnaire_successfully())

        projectsPage = global_navigation.navigate_to_view_all_project_page();
        lightBox = projectsPage.open_activate_project_light_box(VALID_DATA_FOR_PROJECT[PROJECT_NAME])
        lightBox.activate_project()

        add_data_sender_page = global_navigation.navigate_to_all_data_sender_page().navigate_to_add_a_data_sender_page()
        add_data_sender_page.add_data_sender_with(VALID_DATA_FOR_DATA_SENDER)
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)

        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(VALID_SMS_DATA_FROM_DATA_SENDER)
        sleep(60 * 4)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_SMS_DATA_FROM_DATA_SENDER)))



    def tearDown(self):
        try:
            self.driver.quit()
            for email in self.emails:
                dbmanager = DatabaseManager()
                dbname = dbmanager.delete_organization_all_details(email)
                couchwrapper = CouchHttpWrapper("localhost")
                couchwrapper.deleteDb(dbname)
            pass
        except TypeError as e:
            pass

#def test_send_SMS_to_paid_accounts_check_results(self):


# vim: ai ts=4 sts=4 et sw=4utf-8
import time
from nose.plugins.attrib import attr
from framework.base_test import BaseTest
from framework.utils.common_utils import get_epoch_last_ten_digit
from framework.utils.couch_http_wrapper import CouchHttpWrapper
from framework.utils.data_fetcher import from_, fetch_
from framework.utils.database_manager_postgres import DatabaseManager
from pages.activateaccountpage.activate_account_page import ActivateAccountPage
from pages.addsubjecttypepage.add_subject_type_page import AddSubjectTypePage
from pages.loginpage.login_page import LoginPage
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_SMS_TESTER_PAGE, DATA_WINNER_DASHBOARD_PAGE
from tests.endtoendtest.end_to_end_data import *


class TestIntregationOfApplication(BaseTest):
    def tearDown(self):
        try:
            self.driver.quit()
            if self.email is not None:
                email = self.email
                dbmanager = DatabaseManager()
                dbname = dbmanager.delete_organization_all_details(email)
                couchwrapper = CouchHttpWrapper("localhost")
                couchwrapper.deleteDb(dbname)
        except TypeError as e:
            pass

    def activate_account(self):
        account_activate_page = ActivateAccountPage(self.driver)
        dbmanager = DatabaseManager()
        activation_code = dbmanager.get_activation_code(self.email)
        account_activate_page.activate_account(activation_code)
        self.assertRegexpMatches(account_activate_page.get_message(),
                                 fetch_(SUCCESS_MESSAGE, from_(VALID_ACTIVATION_DETAILS)))

    def set_organization_number(self):
        dbmanager = DatabaseManager()
        organization_sms_tel_number = get_epoch_last_ten_digit()
        dbmanager.set_sms_telephone_number(organization_sms_tel_number, self.email)
        return organization_sms_tel_number

    def do_org_registartion(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        registration_page = login_page.navigate_to_registration_page()
        self.assertEqual(self.driver.get_title(), "Register")
        registration_confirmation_page, self.email = registration_page.successful_registration_with(
            REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)
        self.assertEquals(registration_confirmation_page.registration_success_message(),
                          fetch_(SUCCESS_MESSAGE, from_(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)))

    def do_login(self, valid_credentials):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        valid_credentials[USERNAME] = self.email
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(valid_credentials)
        self.assertEqual(global_navigation.welcome_message(), fetch_(WELCOME_MESSAGE, from_(valid_credentials)))
        return global_navigation

    def add_a_data_sender(self, dashboard_page):
        add_data_sender_page = dashboard_page.navigate_to_add_data_sender_page()
        add_data_sender_page.add_data_sender_with(VALID_DATA_FOR_DATA_SENDER)
        self.assertRegexpMatches(add_data_sender_page.get_success_message(),
                                 fetch_(SUCCESS_MESSAGE, from_(VALID_DATA_FOR_DATA_SENDER)))

    def add_subject_type(self, create_project_page, valid_subject_type):
        add_subject_type_page = AddSubjectTypePage(self.driver)
        add_subject_type_page.click_on_accordian_link()
        add_subject_type_page.add_entity_type_with(valid_subject_type)
        entity_type = fetch_(ENTITY_TYPE, from_(valid_subject_type))
        time.sleep(2)
        self.assertEqual(create_project_page.get_selected_subject(), entity_type.lower())

    def add_a_subject(self, add_subject_page):
        message = add_subject_page.successfully_add_subject_with(VALID_DATA_FOR_SUBJECT)
        self.assertEqual(add_subject_page.get_flash_message(), message)

    def add_a_data_sender(self, add_data_sender_page):
        add_data_sender_page.add_data_sender_with(VALID_DATA_FOR_DATA_SENDER)
        self.assertEqual(add_data_sender_page.get_success_message(),
                         fetch_(SUCCESS_MESSAGE, from_(VALID_DATA_FOR_DATA_SENDER)))

    def create_project(self, create_project_page):
        create_project_page.create_project_with(VALID_DATA_FOR_PROJECT)
        create_subject_questionnaire_page = create_project_page.save_project_successfully()
        self.assertEqual(self.driver.get_title(),
                         fetch_(PAGE_TITLE, from_(VALID_DATA_FOR_PROJECT)))
        return create_subject_questionnaire_page

    def create_subject_questionnaire(self, create_subject_questionnaire_page):
        create_questionnaire_page = create_subject_questionnaire_page.save_questionnaire_successfully()
        self.assertRegexpMatches(self.driver.get_title(),
                                 fetch_(PAGE_TITLE, from_(VALID_DATA_FOR_SUBJECT_QUESTIONNAIRE)))
        return create_questionnaire_page

    def create_data_sender_questionnaire(self, create_data_sender_questionnaire_page):
        reminder_page = create_data_sender_questionnaire_page.save_questionnnaire_successfully()
        self.assertRegexpMatches(self.driver.get_title(),
                                 fetch_(PAGE_TITLE, from_(VALID_DATA_FOR_DATA_SENDER_QUESTIONNAIRE)))
        return reminder_page

    def create_reminder(self, reminder_page):
        review_and_test_page = reminder_page.save_reminder_successfully()
        self.assertRegexpMatches(self.driver.get_title(),
                                 fetch_(PAGE_TITLE, from_(VALID_DATA_FOR_REMINDER)))
        return review_and_test_page

    def create_questionnaire(self, create_questionnaire_page):
        create_questionnaire_page.create_questionnaire_with(QUESTIONNAIRE_DATA)
        index = 2
        for question in fetch_(QUESTIONS, from_(QUESTIONNAIRE_DATA)):
            question_link_text = fetch_(QUESTION, from_(question)) + " " + fetch_(CODE, from_(question))
            self.assertEquals(create_questionnaire_page.get_question_link_text(index), question_link_text)
            index += 1
        time.sleep(5)
        self.assertEquals(create_questionnaire_page.get_remaining_character_count(),
                          fetch_(CHARACTER_REMAINING, from_(QUESTIONNAIRE_DATA)))
        create_data_sender_questionnaire_page = create_questionnaire_page.save_questionnaire_successfully()
        return create_data_sender_questionnaire_page

    def send_sms(self, organization_sms_tel_number):
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_data = VALID_DATA_FOR_SMS
        sms_tester_data[RECEIVER] = str(organization_sms_tel_number)
        sms_tester_page.send_sms_with(sms_tester_data)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(SUCCESS_MESSAGE, from_(sms_tester_data)))
        return sms_tester_page

    def verify_submission(self, global_navigation):
        view_all_project_page = global_navigation.navigate_to_view_all_project_page()
        project_overview_project = view_all_project_page.navigate_to_project_overview_page(
            fetch_(PROJECT_NAME, VALID_DATA_FOR_PROJECT))
        data_page = project_overview_project.navigate_to_data_page()
        submission_log_page = data_page.navigate_to_all_data_record_page()
        self.assertRegexpMatches(submission_log_page.get_submission_message(SMS_DATA_LOG),
                                 fetch_(SMS_SUBMISSION, from_(SMS_DATA_LOG)))

    @attr('functional_test', 'smoke', "intregation")
    def test_end_to_end(self):
        self.email = None
        self.do_org_registartion()

        organization_sms_tel_number = self.set_organization_number()
        self.activate_account()
        global_navigation = self.do_login(VALID_CREDENTIALS)

        dashboard_page = global_navigation.navigate_to_dashboard_page()
        create_project_page = dashboard_page.navigate_to_create_project_page()
        self.add_subject_type(create_project_page, VALID_SUBJECT_TYPE2)
        self.add_subject_type(create_project_page, VALID_SUBJECT_TYPE1)
        create_subject_questionnaire_page = self.create_project(create_project_page)
        create_questionnaire_page = self.create_subject_questionnaire(create_subject_questionnaire_page)
        create_data_sender_questionnaire_page = self.create_questionnaire(create_questionnaire_page)
        reminder_page = self.create_data_sender_questionnaire(create_data_sender_questionnaire_page)
        review_and_test_page = self.create_reminder(reminder_page)

        all_subjects_page = global_navigation.navigate_to_all_subject_page()
        add_subject_page = all_subjects_page.navigate_to_add_a_subject_page()
        self.add_a_subject(add_subject_page)

        all_data_senders_page = global_navigation.navigate_to_all_data_sender_page()
        add_data_sender_page = all_data_senders_page.navigate_to_add_a_data_sender_page()
        self.add_a_data_sender(add_data_sender_page)

        all_projects_page = global_navigation.navigate_to_view_all_project_page()
        project_name = fetch_(PROJECT_NAME, from_(VALID_DATA_FOR_PROJECT))
        activate_project_light_box = all_projects_page.open_activate_project_light_box(project_name)
        self.assertEqual(activate_project_light_box.get_title_of_light_box(), "Activate this Project?")
        project_overview_page = activate_project_light_box.activate_project()
        self.assertEqual(project_overview_page.get_status_of_the_project(), "Active")

        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        self.send_sms(organization_sms_tel_number)

        self.driver.go_to(DATA_WINNER_DASHBOARD_PAGE)
        self.verify_submission(global_navigation)

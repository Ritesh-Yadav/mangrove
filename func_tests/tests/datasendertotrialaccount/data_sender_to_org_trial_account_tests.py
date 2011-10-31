from testdata.test_data import DATA_WINNER_SMS_TESTER_PAGE, DATA_WINNER_LOGIN_PAGE
from framework.base_test import BaseTest
from data_sender_to_org_trial_account_data import VALID_DATA, PROJECT_NAME, TRIAL_SMS_DATA, VALID_PAID_DATA, PAID_SMS_DATA
from pages.loginpage.login_page import LoginPage
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from tests.logintests.login_data import TRIAL_CREDENTIALS_TWO, VALID_CREDENTIALS
from nose.plugins.attrib import attr
from framework.utils.couch_http_wrapper import CouchHttpWrapper
import json


# add data sender to trial account

# add data sender to paid account

# send sms to trial one
    #check sms submission in this trail display, not paid display

# send sms to paid account
    #check sms submission paid paid display, not paid display


class TestDataSenderAssociationWithTrialAccount(BaseTest):

    @attr('functional_test', 'smoke')
    def test_data_sender_registered_to_paid_and_trial_accounts_send_SMS_to_trial_accounts_check_results(self):
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(VALID_DATA)

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(TRIAL_CREDENTIALS_TWO)
        all_data_page = global_navigation.navigate_to_all_data_page()
        analysis_page = all_data_page.navigate_to_data_analysis_page(PROJECT_NAME)
        data_rows = analysis_page.get_data_rows()
        row_data = analysis_page.get_data_from_row(data_rows[0])
        self.assertEqual(row_data, TRIAL_SMS_DATA)

    @attr('functional_test')
    def test_data_sender_registered_to_paid_and_trial_accounts_send_SMS_to_trial_account_check_absent_from_paid(self):
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(VALID_DATA)

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(VALID_CREDENTIALS)
        all_data_page = global_navigation.navigate_to_all_data_page()
        analysis_page = all_data_page.navigate_to_data_analysis_page(PROJECT_NAME)

        data_rows = analysis_page.get_all_data_records()
        analysis_page.go_to_next_page()
        data_rows.extend(analysis_page.get_all_data_records())
        for row_data in data_rows:
            self.assertNotEqual(row_data, TRIAL_SMS_DATA)

    @attr('functional_test')
    def test_data_sender_registered_to_paid_and_trial_accounts_send_SMS_to_paid_account_check_results(self):
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(VALID_PAID_DATA)

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(VALID_CREDENTIALS)
        all_data_page = global_navigation.navigate_to_all_data_page()
        analysis_page = all_data_page.navigate_to_data_analysis_page(PROJECT_NAME)

        data_rows = analysis_page.get_all_data_records()
        analysis_page.go_to_next_page()
        data_rows.extend(analysis_page.get_all_data_records())
        sms_exist = False
        for row_data in data_rows:
            if row_data==PAID_SMS_DATA:
                sms_exist = True
                break
        self.assertTrue(sms_exist)

    def tearDown(self):
        self.driver.close()
        couchdb_wrapper = CouchHttpWrapper("localhost")
        json_data = couchdb_wrapper.get("/hni_testorg_coj00001/_design/submissionlog/_view/submissionlog?reduce=false")
        json_parsed_data = json.load(json_data)
        for data in range(json_parsed_data["total_rows"]):
            id = json_parsed_data["rows"][data]["id"]
            rev = json_parsed_data["rows"][data]["value"]["_rev"]
            couchdb_wrapper.delete("/hni_testorg_coj00001/"+id+"?rev="+rev)

#def test_send_SMS_to_paid_accounts_check_results(self):


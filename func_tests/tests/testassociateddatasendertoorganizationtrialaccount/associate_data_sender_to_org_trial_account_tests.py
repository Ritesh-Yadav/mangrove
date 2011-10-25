#from pages.smstesterpage.sms_tester_page import SMSTesterPage
#from testdata.test_data import DATA_WINNER_SMS_TESTER_PAGE
#from tests.endtoendtest.end_to_end_data import VALID_DATA_FOR_DATA_SENDER
#from tests.endtoendtest.end_to_end_tests import activate_account, do_login
#from tests.registrationtests.registration_data import REGISTRATION_PASSWORD
#from tests.registrationtests.trial_registration_tests import register_and_get_email_for_trial
#from tests.smstestertests.sms_tester_data import VALID_DATA
#
## add data sender to trial account
#
## add data sender to paid account
#
## send sms to trial one
#    #check sms submission in this trail display, not paid display
#
## send sms to paid account
#    #check sms submission paid paid display, not paid display
#
#
#def test_datasender_send_SMS_to_trial_accounts_check_results(self):
#    registration_confirmation_page, email = register_and_get_email_for_trial(self.driver)
#    self.emails.append(email)
#    activate_account(self.driver, email)
#    global_navigation = do_login(self.driver, email, REGISTRATION_PASSWORD)
#    # create a project
#    dashboard_page = global_navigation.navigate_to_dashboard_page()
#    self.create_questionnaire(self.create_project(dashboard_page.navigate_to_create_project_page()).save_questionnaire_successfully())
#
#    add_data_sender_page = global_navigation.navigate_to_all_data_sender_page().navigate_to_add_a_data_sender_page()
#    # MOBILE_NUMBER: "1234567890",
#    add_data_sender_page.add_data_sender_with(VALID_DATA_FOR_DATA_SENDER)
#
#    # send sms
#    self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
#    sms_tester_page = SMSTesterPage(self.driver)
#    #VALID_DATA = {SENDER: "1234567890",
#    #             RECEIVER: "919880734937",
#    #             SMS: "cli009 .EID cid003 .NA Mr. Tessy .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
#    #            SUCCESS_MESSAGE: "Thank you Shweta. We received : EID: cid003 NA: Mr. Tessy FA: 58.0 RD: 17.05.2011 BG: O- SY: Rapid weight loss,Memory loss,Neurological disorders GPS: 27.178057,-78.007789"}
#
#    sms_tester_pfirefoxage.send_sms_with(VALID_DATA)
#
#    self.assertEqual(sms_tester_page.get_response_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_DATA)))
#
#
#def test_send_SMS_to_paid_accounts_check_results(self):
#

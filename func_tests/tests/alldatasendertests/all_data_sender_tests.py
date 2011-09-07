# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import time
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.adddatasenderspage.add_data_senders_page import AddDataSenderPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_CREATE_DATA_SENDERS
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.adddatasenderstests.add_data_senders_data import *


class TestAddDataSender(BaseTest):
    def prerequisites_of_add_data_sender(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.do_successful_login_with(VALID_CREDENTIALS)

        # doing Addition of DataSender
        self.driver.go_to(DATA_WINNER_CREATE_DATA_SENDERS)
        return AddDataSenderPage(self.driver)

    @SkipTest
    @attr('functional_test', 'smoke')
    def test_successful_addition_of_data_sender(self):
        """
        Function to test the successful Addition of DataSender with given
        details e.g. first name, last name, telephone number and commune
        """
        add_data_sender_page = self.prerequisites_of_add_data_sender()
        add_data_sender_page.add_data_sender_with(VALID_DATA)
        self.assertRegexpMatches(add_data_sender_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(VALID_DATA)))
  
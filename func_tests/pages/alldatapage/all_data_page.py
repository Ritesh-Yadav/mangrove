# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import by_xpath
from pages.alldatapage.all_data_locator import *
from pages.page import Page
from pages.submissionlogpage.submission_log_page import SubmissionLogPage


class AllDataPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_all_data_records_page(self, project_name):
        """
        Function to navigate to all data records page of the website

        Return All Data Records page
         """
        self.driver.find(by_xpath(All_DATA_RECORDS_LINK_XPATH % project_name)).click()
        return SubmissionLogPage(self.driver)

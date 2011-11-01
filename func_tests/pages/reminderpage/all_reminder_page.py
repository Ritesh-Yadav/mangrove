# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import time
from framework.utils.common_utils import CommonUtilities
from pages.dataanalysispage.data_analysis_locator import *
from pages.page import Page
from pages.reminderpage.all_reminder_locator import SENT_REMINDERS_LINK, SCHEDULED_REMINDERS_LINK
from pages.submissionlogpage.submission_log_page import SubmissionLogPage
from tests.dataanalysistests.data_analysis_data import CURRENT_MONTH, LAST_MONTH, YEAR_TO_DATE


class AllReminderPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def click_schedule_reminder_tab(self):
        CommonUtilities(self.driver).wait_for_element(3,SCHEDULED_REMINDERS_LINK)
        self.driver.find(SCHEDULED_REMINDERS_LINK).click()

    def click_sent_reminder_tab(self):
        self.driver.find(SENT_REMINDERS_LINK).click()
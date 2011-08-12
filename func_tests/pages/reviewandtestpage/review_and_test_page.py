# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import CommonUtilities, generateId
from pages.page import Page
from pages.projectoverviewpage.project_overview_page import ProjectOverviewPage
from pages.reviewandtestpage.review_and_test_locator import *
from framework.utils.common_utils import *


class ReviewAndTestPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_project_overview_page(self):
        """
        Function to navigate to project overview page of the website

        Return project_overview_page
         """
        self.driver.find(GO_TO_PROJECT_OVERVIEW_BTN).click()
        return ProjectOverviewPage(self.driver)

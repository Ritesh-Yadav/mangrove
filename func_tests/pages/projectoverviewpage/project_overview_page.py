# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.createprojectpage.create_project_page import *
from pages.dataanalysispage.data_analysis_page import DataAnalysisPage
from pages.lightbox.light_box_page import LightBox
from pages.projectoverviewpage.project_overview_locator import *
from pages.page import Page
from pages.smstesterlightbox.sms_tester_light_box_page import SMSTesterLightBoxPage


class ProjectOverviewPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_data_page(self):
        """
        Function to navigate data page

        Return data page
         """
        self.driver.find(DATA_TAB).click()
        return DataAnalysisPage(self.driver)

    def navigate_to_edit_project_page(self):
        """
        Function to navigate to create project page

        Return create project page
         """
        self.driver.find(PROJECT_EDIT_LINK).click()
        return CreateProjectPage(self.driver)

    def open_activate_project_light_box(self):
        """
        Function to open the activate project light box

        Return ActivateProjectLightBox
         """
        self.driver.find(ACTIVATE_PROJECT_LINK).click()
        return LightBox(self.driver)

    def get_status_of_the_project(self):
        """
        Function to get the current status of the project

        Return status
         """
        return self.driver.find(PROJECT_STATUS_LABEL).text

    def open_sms_tester_light_box(self):
        """
        Function to open the SMS tester light box

        Return SMSTesterLightBoxPage
         """
        self.driver.find(TEST_QUESTIONNAIRE_LINK).click()
        return SMSTesterLightBoxPage(self.driver)

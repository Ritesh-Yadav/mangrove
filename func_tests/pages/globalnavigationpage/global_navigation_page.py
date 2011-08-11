# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.globalnavigationpage.global_navigation_locator import *
from pages.page import Page
from pages.projectspage.projects_page import ProjectsPage
from pages.registerreporterpage.register_reporter_page import ReporterRegistrationPage
from pages.registersubjectpage.register_subject_page import RegisterSubjectPage


class GlobalNavigationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def welcome_message(self):
        """
        Function to fetch the Welcome message from the label provided on
        dashboard page.

        Return the Welcome message
         """
        welcome_message = self.driver.find(WELCOME_MESSAGE_LABEL).text
        return welcome_message

    def navigate_to_register_reporter_page(self):
        """
        Function to navigate to register a reporter page of the website.

        Return register reporter page
         """
        self.driver.find(DATA_SENDERS_LINK).click()
        return ReporterRegistrationPage(self.driver)

    def navigate_to_view_all_project_page(self):
        """
        Function to navigate to view all projects page of the website.

        Return view all projects page
         """
        self.driver.find(PROJECT_LINK).click()
        return ProjectsPage(self.driver)

    def navigate_to_all_subject_page(self):
        """
        Function to navigate to register a subject page of the website.

        Return register subject page
         """
        self.driver.find(SUBJECTS_LINK).click()
        return RegisterSubjectPage(self.driver)

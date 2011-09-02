# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.lightbox.light_box_page import LightBox
from pages.createprojectpage.create_project_page import CreateProjectPage
from pages.projectoverviewpage.project_overview_page import ProjectOverviewPage
from pages.projectspage.projects_locator import *
from pages.page import Page


class ProjectsPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_create_project_page(self):
        """
        Function to navigate to create project page of the website.

        Return create project page
         """
        self.driver.find(CREATE_A_NEW_PROJECT_LINK).click()
        return CreateProjectPage(self.driver)

    def navigate_to_project_overview_page(self, project_name):
        """
        Function to navigate to specific project overview page

        Return project overview page
         """
        project_link = by_xpath(PROJECT_LINK_XPATH % project_name.lower())
        self.driver.find(project_link).click()
        return ProjectOverviewPage(self.driver)

    def open_activate_project_light_box(self, project_name):
        """
        Function to open the activate project light box

        Return ActivateProjectLightBox
         """
        self.driver.find(by_xpath(ACTIVATE_PROJECT_LINK_XPATH % project_name.lower())).click()
        return LightBox(self.driver)

    def get_status_of_the_project(self, project_name):
        """
        Function to get the current status of the project

        Return status
         """
        return self.driver.find(by_xpath(PROJECT_STATUS_LABEL_XPATH % project_name.lower())).text

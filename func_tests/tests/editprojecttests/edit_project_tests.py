# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.dashboardpage.dashboard_page import DashboardPage
from pages.loginpage.login_page import LoginPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.editprojecttests.edit_project_data import *


class TestEditProject(BaseTest):

    def prerequisites_of_create_project(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        global_navigation = login_page.do_successful_login_with(VALID_CREDENTIALS)

        # going on all project page
        return global_navigation.navigate_to_view_all_project_page()
    @SkipTest
    @attr('functional_test', 'smoke')
    def test_successful_project_editing(self):
        """
        Function to test the successful creation of project with given
        details e.g. Name, Project Background and goal, Project Type,
        Subject and Devices
        """
        all_project_page = self.prerequisites_of_create_project()
        project_overview_page = all_project_page.navigate_to_project_overview_page(fetch_(PROJECT_NAME ,from_(VALID_DATA)))
        edit_project_page = project_overview_page.navigate_to_edit_project_page()
        self.assertEqual(VALID_DATA ,edit_project_page.get_project_details())
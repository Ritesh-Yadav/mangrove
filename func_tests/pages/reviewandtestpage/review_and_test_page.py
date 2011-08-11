# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import CommonUtilities, generateId
from pages.page import Page
from pages.reviewandtestpage.review_and_test_locator import *
from framework.utils.common_utils import *


class ReviewAndTestPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

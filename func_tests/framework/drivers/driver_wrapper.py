# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from framework.exception import ElementStillPresentException, CouldNotLocatePageException, ElementFoundWithoutDesiredVisibility
from framework.exception import CouldNotLocateElementException
from framework.utils.drop_down_web_element import DropDown
from framework.utils.text_box_web_element import TextBox
from framework.utils.radio_button_web_element import RadioButton
from pages.loginpage.login_locator import *
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def get_default_browser_name():
    import sys
    if os.system('which chromedriver > /dev/null') == os.EX_OK:
        sys.stderr.write("chromedriver found, using chrome as the browser\n")
        return "chrome"
    else:
        sys.stderr.write("chromedriver not found, falling back to firefox\n")
        return "firefox"

def get_driver_for_browser(browser):
    print "Getting driver for browser: ", browser
    if browser == "firefox":
        return webdriver.Firefox()
    elif browser == "ie":
        return webdriver.Ie()
    elif browser == "chrome":
        capabilities = dict(DesiredCapabilities.CHROME, **{
            'chrome.switches': ["--incognito"]
        })
        return webdriver.Chrome(desired_capabilities=capabilities)
    elif browser == "htmlunit":
        return webdriver.Remote()
    else:
        raise NotImplemented("Unknown browser " + browser)

class DriverWrapper(object):
    """
    DriverWrapper class is for creating an wrapper over traditional webdriver
     class. To do some additional function on different web elements
    """

    def __init__(self, browser=get_default_browser_name()):
        self._driver = get_driver_for_browser(browser)

    def find_drop_down(self, locator_dict):
        """
        Create DropDown class object with the given web element

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return DropDown
        """
        return DropDown(self.find(locator_dict))

    def find_text_box(self, locator_dict):
        """
        Create TextBox class object with the given web element

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return TextBox
        """
        return TextBox(self.find(locator_dict))

    def find_radio_button(self, locator_dict):
        """
        Create RadioButton class object with the given web element

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return RadioButton
        """
        return RadioButton(self.find(locator_dict))

    def find(self, locator_dict):
        """
        Finds element on the web page using locator dictionary

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return webelement
        """
        try:
            return self._driver.find_element(by=locator_dict[BY], value=locator_dict[LOCATOR])
        except NoSuchElementException as e:
            raise CouldNotLocateElementException(selector=locator_dict[BY], locator=locator_dict[LOCATOR])

    def find_elements_(self, locator_dict):
        """
        Finds elements on the web page using locator dictionary

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return list of webelement
        """
        return self._driver.find_elements(by=locator_dict[BY],
                                         value=locator_dict[LOCATOR])

    def go_to(self, url):
        """Open URL using get command of webdriver api"""
        self._driver.get(url)

    def get_title(self):
        """Get the title of the web page"""
        return self._driver.title

    def is_element_present(self, element_locator):
        try:
            locator = self.find(element_locator)
            return locator
        except CouldNotLocateElementException:
            return False

    def wait_until_modal_dismissed(self, time_out_in_seconds):
        self.wait_until_element_is_not_present(time_out_in_seconds, by_css(".loading"))

    def wait_for_element(self, time_out_in_seconds, object_id, want_visible=None):
        """Finds elements by their id by waiting till timeout.

        Note that implicitly_wait mostly largely eliminates the need for this"""

        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(0, time_out_in_seconds)

        while True:
            try:
                element = self.find(object_id)
                current_time = datetime.datetime.now()

                if want_visible is None or element.is_displayed() == want_visible:
                    return element
                elif current_time >= end_time:
                    message = "Expected visibility %s for element %s -- found %s after %s seconds" % (want_visible, object_id, element.is_displayed(), time_out_in_seconds)
                    raise ElementFoundWithoutDesiredVisibility(message)
            except CouldNotLocateElementException as ne:
                current_time = datetime.datetime.now()
                if current_time >= end_time:
                    raise ne

    def wait_for_page_with_title(self, time_out_in_seconds, title):
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(0, time_out_in_seconds)

        while True:
            if self.title == title:
                return title
            else:
                current_time = datetime.datetime.now()
                if current_time >= end_time:
                    raise CouldNotLocatePageException("Could not locate page with title %s after %s seconds" % (title, time_out_in_seconds))

    def __getattr__(self, item):
        return getattr(self._driver, item)

    def wait_until_element_is_not_present(self, time_out_in_seconds, locator):
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(0, time_out_in_seconds)

        while True:
            try:
                element = self.find(locator)
                if element and not element.is_displayed():
                    return True
                else:
                    current_time = datetime.datetime.now()
                    if current_time >= end_time:
                        raise ElementStillPresentException("Timer expired and %s is still present" % locator)
            except CouldNotLocateElementException:
                return
            except StaleElementReferenceException:
                return



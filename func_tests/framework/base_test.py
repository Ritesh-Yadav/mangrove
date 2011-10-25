# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import os

import unittest
from framework.drivers.driver_wrapper import DriverWrapper
from tests.testsettings import CLOSE_BROWSER_AFTER_TEST, WAIT


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = DriverWrapper()
        self.driver.implicitly_wait(WAIT)
        self.driver.execute_script("window.innerWidth = screen.width;window.innerHeight = screen.height;window.screenX = 0;window.screenY = 0;alwaysLowered = false;")

    def tearDown(self):
        try:
            if CLOSE_BROWSER_AFTER_TEST:
                self.driver.quit()
        except TypeError as e:
            pass

if __name__ == "__main__":
    unittest.main()

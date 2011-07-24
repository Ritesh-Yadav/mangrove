# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.drivers.driver_initializer import DriverInitializer
import unittest
from tests.testsettings import close_browser_after_test


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = DriverInitializer.initialize("firefox")

    def tearDown(self):
        try:
            if close_browser_after_test:
                self.driver.quit()
        except TypeError as e:
            pass

if __name__ == "__main__":
    unittest.main()

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from selenium.webdriver.remote.webelement import WebElement


class TextBox (WebElement):

    def __init__(self, textBoxWebElement):
        super(TextBox, self).__init__(textBoxWebElement.parent, textBoxWebElement.id)
        self.webElement = textBoxWebElement

    def enter_text(self, textToBeEntered):
        self.webElement.click()
        self.webElement.clear()
        self.webElement.send_keys(textToBeEntered)
        return self

    def is_enabled(self):
        return self.webElement.is_enabled()

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


class Page(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = self.driver.current_url

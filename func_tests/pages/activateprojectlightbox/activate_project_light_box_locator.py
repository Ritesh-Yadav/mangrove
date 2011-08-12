# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.utils.common_utils import *


# By default every locator should be CSS
# Abbr:
# TB - Text Box
# CB - Check Box
# RB - Radio Button
# BTN - Button
# DD - Drop Down
# LINK - Links
# LABEL - Label


# variable to access locators
LOCATOR = "locator"
BY = "by"

ACTIVATE_BTN = by_css("a#confirm")
CANCEL_LINK = by_css("a.cancel_link")
CLOSE_BTN = by_css("span[class='ui-icon ui-icon-closethick']")
MESSAGE_LABEL = by_css("p.warning_message")
TITLE_LABEL = by_xpath("//div[@role='dialog' and contains(@style,'block')]/div/span[@class='ui-dialog-title']")
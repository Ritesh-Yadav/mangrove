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

FIRST_NAME_TB = by_css("input#id_first_name")
MOBILE_NUMBER_TB = by_css("input#id_telephone_number")
COMMUNE_TB = by_css("input#id_location")
GPS_TB = by_css("input#id_geo_code")

REGISTER_BTN = by_css("input#id_register_button")
ERROR_MESSAGE_LABEL = by_xpath("//ul[@class='errorlist']/.. | //div[@id='error_messages']")
FLASH_MESSAGE_LABEL = by_xpath("//div[@class='success-message-box' and @id='flash-message']")

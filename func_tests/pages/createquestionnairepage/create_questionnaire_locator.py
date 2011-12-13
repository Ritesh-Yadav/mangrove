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

QUESTIONNAIRE_CODE_TB = by_css("input#questionnaire-code")
QUESTION_TB = by_xpath("//input[@id='question_title']")
CODE_TB = by_css("input#code")
WORD_OR_PHRASE_RB = by_css("input[value='text']")
NO_CHARACTER_LIMIT_RB = by_xpath(
    "//li[not(contains(@style,'none')) and contains(@data-bind,'showAddTextLength')]/div/input[@value='length_unlimited']")
CHARACTER_LIMIT_RB = by_xpath(
    "//li[not(contains(@style,'none')) and contains(@data-bind,'showAddTextLength')]/div/div/input[@value='length_limited']")
WORD_OR_PHRASE_MAX_LENGTH_TB = by_xpath(
    "//li[not(contains(@style,'none')) and contains(@data-bind,'showAddTextLength')]//../input[@id='max_length' and not(contains(@style,'none'))]")
NUMBER_RB = by_css("input[value='integer']")
NUMBER_MAX_LENGTH_TB = by_xpath(
    "//li[not(contains(@style,'none')) and contains(@data-bind,'showAddRange')]/div/div/input[@id='range_max']")
NUMBER_MIN_LENGTH_TB = by_xpath(
    "//li[not(contains(@style,'none')) and contains(@data-bind,'showAddRange')]/div/div/input[@id='range_min']")

DATE_RB = by_css("input[value='date']")
MONTH_YEAR_RB = by_xpath("//input[@value='mm.yyyy']")
DATE_MONTH_YEAR_RB = by_xpath("//input[@value='dd.mm.yyyy']")
MONTH_DATE_YEAR_RB = by_xpath("//input[@value='mm.dd.yyyy']")

LIST_OF_CHOICE_RB = by_css("input[value='choice']")
CHOICE_XPATH_LOCATOR = "//li[not(contains(@style,'none')) and contains(@data-bind,'showAddChoice')]/div/ol/li"
CHOICE_TB_XPATH_LOCATOR = "/input"
CHOICE_DELETE_LINK_XPATH_LOCATOR = "/p/a[text()='delete']"
ADD_CHOICE_LINK = by_xpath("//li[not(contains(@style,'none')) and contains(@data-bind,'showAddChoice')]/div/a")
ONLY_ONE_ANSWER_RB = by_css("input[value='select1']")
MULTIPLE_ANSWER_RB = by_css("input[value='select']")

GEO_RB = by_css("input[value='geocode']")
CHARACTER_COUNT = by_css("div#char-count")
BACK_BTN = by_css("input#back_to_project")

PREVIOUS_STEP_LINK = by_xpath("//a[@id='subjects_link' and text()='Subjects']")

# Locators for Question List section of the page
DEFAULT_QUESTION_LINK = by_xpath(
    "//div[@class='question_list']/ol/li[1]/a[1]")
QUESTION_LINK_CSS_LOCATOR_PART1 = "div.question_list>ol>li"  # index number to identify question
QUESTION_LINK_CSS_LOCATOR_PART2 = ">a"  # Add text to locate specific question
QUESTION_DELETE_LINK_CSS_LOCATOR_PART1 = "div.question_list>ol>li>a"  # Add text or index number to identify question
QUESTION_DELETE_LINK_CSS_LOCATOR_PART1 = "~div>span.delete>a"
ADD_A_QUESTION_LINK = by_css("div.add_question>a")
SAVE_CHANGES_BTN = by_css("input#submit-button[value='Next Step: Data Senders']")

SUCCESS_MESSAGE_LABEL = by_xpath(
    "//div[@id='message-label']/label[@class='success_message' and not(contains(@style,'none'))]")

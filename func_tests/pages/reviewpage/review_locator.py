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

PROJECT_ACCORDION = by_css("div#project_profile>div[class~='ui-state-default']")
PROJECT_NAME_LABEL = by_css("div[class~='ui-accordion-content-active'] p#project_name")
PROJECT_TYPE_LABEL = by_css("div[class~='ui-accordion-content-active'] p#project_type")
PROJECT_DESCRIPTION_LABEL = by_css("div[class~='ui-accordion-content-active'] p#project_description")
DEVICES_LABEL = by_css("div[class~='ui-accordion-content-active'] p#devices")
EDIT_PROJECT_LINK = by_css("div[class~='ui-accordion-content-active']>a#project_edit_link")

SUBJECTS_ACCORDION = by_css("div#subjects>div[class~='ui-state-default']")
SUBJECT_TYPE_LABEL = by_css("div[class~='ui-accordion-content-active'] p#subject_type")
SUBJECT_COUNT_LABEL = by_css("div[class~='ui-accordion-content-active'] p#no_of_subjects")
EDIT_SUBJECT_LINK = by_css("div[class~='ui-accordion-content-active']>a#subjects_edit_link")

QUESTIONNAIRE_ACCORDION = by_css("div#questionnaire>div[class~='ui-state-default']")
QUESTIONS_LABELS = by_css("div[class~='ui-accordion-content-active'] p#question")
EDIT_QUESTIONNAIRE_LINK = by_css("div[class~='ui-accordion-content-active']>a#questionnaire_edit_link")

DATA_SENDERS_ACCORDION = by_css("div#data_senders>div[class~='ui-state-default']")
DATA_SENDERS_COUNT_LABEL = by_css("div[class~='ui-accordion-content-active'] p#no_of_datasenders")
EDIT_DATA_SENDER_LINK = by_css("div[class~='ui-accordion-content-active']>a#datasenders_edit_link")

REMINDERS_ACCORDION = by_css("div#reminders>div[class~='ui-state-default']")
EDIT_REMINDER_LINK = by_css("div[class~='ui-accordion-content-active']>a#remider_edit_link")

SMS_QUESTIONNAIRE_LINK = by_css("a#sms_tester")
DATA_SENDERS_PREVIEW_LINK = by_css("a.preview_sender_registration_form")
SUBJECTS_PREVIEW_LINK = by_css("a.preview_subject_registration_form")
WEB_QUESTIONNAIRE_PREVIEW_LINK = by_css("a[class='preview_questionnaire preview']")

GO_TO_PROJECT_OVERVIEW_BTN = by_css("input#submit-button[value='Go to Project Overview']")

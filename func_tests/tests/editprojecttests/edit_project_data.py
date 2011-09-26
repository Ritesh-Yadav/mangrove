# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
from tests.createquestionnairetests.create_questionnaire_data import QUESTIONS

TITLE = "title"
MESSAGE = "message"
PROJECT_NAME = "project_name"
PROJECT_BACKGROUND = "project_background"
PROJECT_TYPE = "project_type"
REPORT_TYPE = "report_type"
SUBJECT = "subject"
DEVICES = "devices"
ERROR_MSG = "message"
PAGE_TITLE = "page_title"
GEN_RANDOM = "gen_random"
DATA_SENDER_WORK = "data sender work"
OTHER_SUBJECT = "other subject"
DEFAULT_QUESTION = "default_question"

VALID_DATA = {PROJECT_NAME: u"clinic3 test project",
              PROJECT_BACKGROUND: u"This project is for automation",
              PROJECT_TYPE: "survey",
              SUBJECT: u"clinic",
              REPORT_TYPE: OTHER_SUBJECT,
              DEVICES: "sms"}

WATER_POINT_DATA = {PROJECT_NAME: u"water point morondova",
                    PROJECT_BACKGROUND: u"This project is for automation",
                    PROJECT_TYPE: "survey",
                    SUBJECT: u"waterpoint",
                    REPORT_TYPE: OTHER_SUBJECT,
                    DEVICES: "sms"}

QUESTIONNAIRE_DATA_FOR_WATER_POINT = {DEFAULT_QUESTION: "q1 Which subject are you reporting on?"}

VALID_DATA2 = {PROJECT_NAME: u"clinic4 test project",
               PROJECT_BACKGROUND: u"This project is for automation",
               PROJECT_TYPE: "survey",
               SUBJECT: u"clinic",
               REPORT_TYPE: OTHER_SUBJECT,
               DEVICES: "sms"}

REPORTER_ACTIVITIES_DATA = {PROJECT_NAME: u"reporter activities",
                            PROJECT_BACKGROUND: u"This project is created by automation",
                            PROJECT_TYPE: "survey",
                            SUBJECT: "",
                            REPORT_TYPE: DATA_SENDER_WORK,
                            DEVICES: "sms"}

QUESTIONNAIRE_DATA_FOR_REPORTER_ACTIVITIES = {QUESTIONS: ["q1 Which subject are you reporting on?", "q2 What is the reporting period for the activity?"]}

LIGHT_BOX_DATA = {TITLE: "Warning !!",
                  MESSAGE: "Warning: Updating the associated type of the project questionnaire will remove all existing data."}

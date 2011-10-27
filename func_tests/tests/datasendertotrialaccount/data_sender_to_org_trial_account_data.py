
DATA_SENDER_NAME = "name"
MOBILE_NUMBER = "mobile_number"
COMMUNE = "commune"
GPS = "gps"
SUCCESS_MESSAGE = "message"

SENDER = "from"
RECEIVER = "to"
SMS = "sms"

QUESTIONNAIRE_CODE = "questionnaire_code"
GEN_RANDOM = "gen_random"
DEFAULT_QUESTION = "default_question"
QUESTION = "question"
QUESTIONS = "questions"
CODE = "code"
TYPE = "type"
LIMIT = "limit"
NO_LIMIT = "no_limit"
LIMITED = "limited"
MIN = "min"
MAX = "max"
DATE_FORMAT = "date_format"
CHOICE = "choice"
ALLOWED_CHOICE = "allowed_choice"
NUMBER = "number"
WORD = "word"
DATE = "date"
LIST_OF_CHOICES = "list_of_choices"
GEO = "geo"
DD_MM_YYYY = "dd.mm.yyyy"
MM_DD_YYYY = "mm.dd.yyyy"
MM_YYYY = "mm.yyyy"
ONLY_ONE_ANSWER = "only_one_answer"
MULTIPLE_ANSWERS = "multiple_answers"
CHARACTER_REMAINING = "character_remaining"
PAGE_TITLE = "page_title"
PROJECT_NAME = "project_name"
RESPONSE_MESSAGE = "message"
MESSAGE = "message"

PROJECT_NAME = "project_name"
SMS = "sms"
RESPONSE_MESSAGE = "message"
PROJECT_BACKGROUND = "project_background"
SUBJECT = "subject"
PROJECT_TYPE = "project_type"
REPORT_TYPE = "report_type"
DEVICES = "devices"


VALID_DATA_FOR_DATA_SENDER = {DATA_SENDER_NAME: "Shweta",
                              MOBILE_NUMBER: "12121212",
                              COMMUNE: "urbaine",
                              GPS: "48.955267  1.816013",
                              SUCCESS_MESSAGE: u"Registration successful. Unique identification number(ID) is: rep2."}

VALID_SMS_DATA_FROM_DATA_SENDER = {SENDER: "12121212",
              RECEIVER: "1-775-237-4679",
              SMS: "WWWW .q1 12.11.2000 .WL 20 .DMY 23.11.2011",
              SUCCESS_MESSAGE: "Thank you Shweta. We received : q1: 12.11.2000 WL: 20.0 DMY: 23.11.2011 eid: rep2"}


QUESTIONNAIRE_DATA = {QUESTIONNAIRE_CODE: "WWWW", GEN_RANDOM: False,
                      DEFAULT_QUESTION: {QUESTION: "What are you reporting on?", CODE: "WID"},
                      QUESTIONS: [{QUESTION: "Water Level", CODE: "WL", TYPE: NUMBER, MIN: "1", MAX: "1000"},
                              {QUESTION: "Date of report in DD.MM.YYYY format", CODE: "DMY", TYPE: DATE,
                               DATE_FORMAT: DD_MM_YYYY}],
                      CHARACTER_REMAINING: "127 / 160 characters used",
                      PAGE_TITLE: "Data Senders"}


VALID_DATA_FOR_PROJECT = {PROJECT_NAME: "Waterpoint morondava", GEN_RANDOM: False,
                          PROJECT_BACKGROUND: "This project is created by functional automation suite.",
                          PROJECT_TYPE: "survey",
                          SUBJECT:"",
                          REPORT_TYPE: "data sender work",
                          DEVICES: "sms",
                          PAGE_TITLE: "Subjects"}



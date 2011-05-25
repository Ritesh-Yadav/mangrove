# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
SENDER = "to"
RECEIVER = "from"
SMS = "sms"
ERROR_MSG = "message"
SUCCESS_MESSAGE = "message"
MESSAGE = "message"

VALID_DATA = {SENDER: "1234567890",
              RECEIVER: "0987654321",
              SMS: "CLI001 +EID CID003 +NA Mr. Tessy +FA 58 +RD 17.05.2011 +BG b +SY ade",
              SUCCESS_MESSAGE: "Thank You Shweta for your submission."}

VALID_DATA2 = {SENDER: "1234567890",
              RECEIVER: "0987654321",
              SMS: "CLI002 +EID CID005 +NA Mr. Tessy +FA 58 +RD 17.05.2011 +BG b +SY ade",
              SUCCESS_MESSAGE: "Thank You Shweta for your submission."}

EXCEED_NAME_LENGTH = {SENDER: "1234567890",
              RECEIVER: "0987654321",
              SMS: "CLI001 +EID CID003 +NA Mr. O'brain +FA 58 +RD 17.05.2011 +BG b +SY ade",
              ERROR_MSG: "Answer Mr. O'brain for question NA is longer than allowed."}

EXCEED_NAME_LENGTH2 = {SENDER: "1234567890",
              RECEIVER: "0987654321",
              SMS: "CLI002 +EID CID005 +NA Mr. O'brain +FA 58 +RD 17.05.2011 +BG b +SY ade",
              ERROR_MSG: "Answer Mr. O'brain for question NA is longer than allowed."}

BLANK_FIELDS = {SENDER: "ddddd",
              RECEIVER: "",
              SMS: "",
              ERROR_MSG: "From *   This field is required.To *   This field is required.SMS *   This field is required."}

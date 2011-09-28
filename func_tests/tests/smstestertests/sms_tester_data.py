# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
SENDER = "from"
RECEIVER = "to"
SMS = "sms"
ERROR_MSG = "message"
SUCCESS_MESSAGE = "message"
MESSAGE = "message"

SUCCESS_MESSAGE_TEXT = "Thank you Shweta for your data record. We successfully received your submission."

VALID_DATA = {SENDER: "1234567890",
              RECEIVER: "919880734937",
              SMS: "cli009 .EID cid003 .NA Mr. Tessy .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
              SUCCESS_MESSAGE: "Thank you Shweta. We received : SY: Rapid weight loss,Memory loss,Neurological disorders BG: O- NA: Mr. Tessy RD: 17.05.2011 FA: 58.0 EID: cid003 GPS: 27.178057,-78.007789"}

VALID_DATA2 = {SENDER: "1234567890",
               RECEIVER: "919880734937",
               SMS: "cli002 .EID cid005 .NA Mr. Tessy .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
               SUCCESS_MESSAGE: "Thank you Shweta. We received : SY: Rapid weight loss,Memory loss,Neurological disorders BG: O- NA: Mr. Tessy RD: 17.05.2011 FA: 58.0 EID: cid005 GPS: 27.178057,-78.007789"}

EXCEED_NAME_LENGTH = {SENDER: "1234567890",
                      RECEIVER: "919880734937",
                      SMS: "cli009 .EID CID003 .NA Mr. O'brain .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
                      ERROR_MSG: "Error. Invalid Submission. Refer to printed Questionnaire. Resend the question ID and answer for na"}

EXCEED_NAME_LENGTH2 = {SENDER: "1234567890",
                       RECEIVER: "919880734937",
                       SMS: "cli002 .EID CID005 .NA Mr. O'brain .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
                       ERROR_MSG: "Error. Invalid Submission. Refer to printed Questionnaire. Resend the question ID and answer for na"}

BLANK_FIELDS = {SENDER: "",
                RECEIVER: "",
                SMS: "",
                ERROR_MSG: "From * This field is required.To * This field is required.SMS * This field is required."}

EXTRA_PLUS_IN_BTW = {SENDER: "1234567890",
                     RECEIVER: "919880734937",
                     SMS: "cli002 .EID cid002 . .NA Mr. Dessy .FA 58 .. .RD 17.05.2011 .BG b .SY ade .  .GPS 27.178057  -78.007789",
                     ERROR_MSG: "Thank you Shweta. We received : SY: Rapid weight loss,Memory loss,Neurological disorders BG: O- NA: Mr. Dessy RD: 17.05.2011 FA: 58.0 EID: cid002 GPS: 27.178057,-78.007789"}

PLUS_IN_THE_BEGINNING = {SENDER: "1234567890",
                         RECEIVER: "919880734937",
                         SMS: ". .cli002 .EID CID005 .NA Mr. Fessy .FA 58 .RD 17.05.2011 .BG b .SY ade",
                         ERROR_MSG: "Error: Invalid Submission. Locate the Questionnaire Code on the printed questionnaire and resend SMS starting with the Questionnaire Code"}

UNREGISTERED_FROM_NUMBER = {SENDER: "123445567",
                            RECEIVER: "919880734937",
                            SMS: "cli002 .EID CID005 . .NA Mr. Kessy .FA 58 .RD 17.05.2011 .BG b .SY ade",
                            ERROR_MSG: "This telephone number is not registered in our system. Please register or contact us at 033 20 426 89."}

REGISTER_DATA_SENDER = {SENDER: "1234567890",
                        RECEIVER: "919880734937",
                        SMS: "REG .t Reporter .m 0123456789 .L  Jaipur .g 26.917 75.817 .N Donald Duck",
                        ERROR_MSG: "Registration successful. Unique identification number\(ID\) is: rep\d.We received : g: 26.917,75.817 m: 0123456789 l: jaipur n: Donald Duck s: rep\d t: Reporter"}

REGISTER_DATA_SENDER_FROM_UNKNOWN_NUMBER = {SENDER: "12345678453",
                                            RECEIVER: "919880734937",
                                            SMS: "REG .t Reporter .m 0123456789 .L   Jaipur .g 26.917 75.817 .N Mr. McDuck",
                                            ERROR_MSG: "This telephone number is not registered in our system. Please register or contact us at 033 20 426 89."}

REGISTER_NEW_SUBJECT = {SENDER: "1234567890",
                        RECEIVER: "919880734937",
                        SMS: "REG .T Clinic .m   123456 .l Jaipur .G 26.917 75.817 ..  .n Clinic Jaipur .S CLIJPR . ",
                        ERROR_MSG: "Registration successful. Unique identification number(ID) is: clijpr.We received : g: 26.917,75.817 m: 123456 l: jaipur n: Clinic Jaipur s: CLIJPR t: Clinic"}

REGISTER_EXISTING_SUBJECT_SHORT_CODE = {SENDER: "1234567890",
                                        RECEIVER: "919880734937",
                                        SMS: "REG .T Clinic .m   123456 .l Jaipur .G 26.917 75.817 ..  .n Clinic Jaipur .S cid001 . ",
                                        ERROR_MSG: "Entity with Unique Identification Number (ID) = cid001 already exists."}

REGISTER_INVALID_GEO_CODE = {SENDER: "1234567890",
                             RECEIVER: "919880734937",
                             SMS: "REG .T Clinic .m   123456 .l Agra .G 127.178057 -78.007789 .n Clinic Agra .S CLIAGRA",
                             ERROR_MSG: "Error. Invalid Submission. Refer to printed Questionnaire. Resend the question ID and answer for g"}

WITH_INVALID_GEO_CODE_FORMAT = {SENDER: "1234567890",
                                RECEIVER: "919880734937",
                                SMS: 'cli002 .EID cid002 . .NA Mr. De`Melo .FA 58 .RD 17.05.2011 .BG ab .SY ade .GPS 127.178057  -78.007789',
                                ERROR_MSG: "Error. Invalid Submission. Refer to printed Questionnaire. Resend the question ID and answer for na, bg, gps"}

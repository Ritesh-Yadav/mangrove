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
              SUCCESS_MESSAGE: "Thank you Shweta. We received : EID: cid003 NA: Mr. Tessy FA: 58.0 RD: 17.05.2011 BG: O- SY: Rapid weight loss,Memory loss,Neurological disorders GPS: 27.178057,-78.007789"}

VALID_DATA2 = {SENDER: "1234567890",
               RECEIVER: "919880734937",
               SMS: "cli002 .EID cid005 .NA Mr. Tessy .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
               SUCCESS_MESSAGE: "Thank you Shweta. We received : EID: cid005 NA: Mr. Tessy FA: 58.0 RD: 17.05.2011 BG: O- SY: Rapid weight loss,Memory loss,Neurological disorders GPS: 27.178057,-78.007789"}

EXCEED_NAME_LENGTH = {SENDER: "1234567890",
                      RECEIVER: "919880734937",
                      SMS: "cli009 .EID CID003 .NA Mr. O'brain .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
                      ERROR_MSG: "Error. Incorrect answer for question na. Please resend entire message."}

EXCEED_NAME_LENGTH2 = {SENDER: "1234567890",
                       RECEIVER: "919880734937",
                       SMS: "cli002 .EID CID005 .NA Mr. O'brain .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
                       ERROR_MSG: "Error. Incorrect answer for question na. Please resend entire message."}

BLANK_FIELDS = {SENDER: "",
                RECEIVER: "",
                SMS: "",
                ERROR_MSG: "From * This field is required.To * This field is required.SMS * This field is required."}

EXTRA_PLUS_IN_BTW = {SENDER: "1234567890",
                     RECEIVER: "919880734937",
                     SMS: "cli002 .EID cid002 . .NA Mr. Dessy .FA 58 .. .RD 17.05.2011 .BG b .SY ade .  .GPS 27.178057  -78.007789",
                     ERROR_MSG: "Thank you Shweta. We received : EID: cid002 NA: Mr. Dessy FA: 58.0 RD: 17.05.2011 BG: O- SY: Rapid weight loss,Memory loss,Neurological disorders GPS: 27.178057,-78.007789"}

PLUS_IN_THE_BEGINNING = {SENDER: "1234567890",
                         RECEIVER: "919880734937",
                         SMS: ". .cli002 .EID CID005 .NA Mr. Fessy .FA 58 .RD 17.05.2011 .BG b .SY ade",
                         ERROR_MSG: "Error with Questionnaire code .. Find the Questionnaire code on the printed questionnaire and resend SMS starting with this questionnaire code."}

UNREGISTERED_FROM_NUMBER = {SENDER: "123445567",
                            RECEIVER: "919880734937",
                            SMS: "cli002 .EID CID005 . .NA Mr. Kessy .FA 58 .RD 17.05.2011 .BG b .SY ade",
                            ERROR_MSG: "Your telephone number is not yet registered in our system. Please contact your supervisor."}

REGISTER_DATA_SENDER = {SENDER: "1234567890",
                        RECEIVER: "919880734937",
                        SMS: "REG .t Reporter .m 0123456789 .L  Jaipur .g 26.917 75.817 .N Donald Duck",
                        ERROR_MSG: "Registration successful. Unique identification number\(ID\) is: rep[\d]+.We received : t: Reporter m: 0123456789 l: jaipur g: 26.917,75.817 n: Donald Duck s: rep[\d]+"}

REGISTER_DATA_SENDER_FROM_UNKNOWN_NUMBER = {SENDER: "12345678453",
                                            RECEIVER: "919880734937",
                                            SMS: "REG .t Reporter .m 0123456789 .L   Jaipur .g 26.917 75.817 .N Mr. McDuck",
                                            ERROR_MSG: "Your telephone number is not yet registered in our system. Please contact your supervisor."}

REGISTER_NEW_SUBJECT = {SENDER: "1234567890",
                        RECEIVER: "919880734937",
                        SMS: "REG .T Clinic .m   123456 .l Jaipur .G 26.917 75.817 ..  .n Clinic Jaipur .S CLIJPR . ",
                        ERROR_MSG: "Registration successful. Unique identification number(ID) is: clijpr.We received : t: Clinic m: 123456 l: jaipur g: 26.917,75.817 n: Clinic Jaipur s: CLIJPR"}

REGISTER_EXISTING_SUBJECT_SHORT_CODE = {SENDER: "1234567890",
                                        RECEIVER: "919880734937",
                                        SMS: "REG .T Clinic .m   123456 .l Jaipur .G 26.917 75.817 ..  .n Clinic Jaipur .S cid001 . ",
                                        ERROR_MSG: "Entity with Unique Identification Number (ID) = cid001 already exists."}

REGISTER_INVALID_GEO_CODE = {SENDER: "1234567890",
                             RECEIVER: "919880734937",
                             SMS: "REG .T Clinic .m   123456 .l Agra .G 127.178057 -78.007789 .n Clinic Agra .S CLIAGRA",
                             ERROR_MSG: "Error. Incorrect answer for question g. Please resend entire message."}

WITH_INVALID_GEO_CODE_FORMAT = {SENDER: "1234567890",
                                RECEIVER: "919880734937",
                                SMS: 'cli002 .EID cid002 . .NA Mr. De`Melo .FA 58 .RD 17.05.2011 .BG ab .SY ade .GPS 127.178057  -78.007789',
                                ERROR_MSG: "Error. Incorrect answer for question na, bg, gps. Please resend entire message."}


# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
PROJECT_NAME = "project_name"
SMS = "sms"
RESPONSE_MESSAGE = "message"
MESSAGE = "message"

PROJECT_DATA = {PROJECT_NAME: "clinic5 test project"}

VALID_DATA = {SMS: "cli005 .EID cid003 .NA Mr. Tessy .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
              RESPONSE_MESSAGE: "Thank you TEST. We received : SY: Rapid weight loss,Memory loss,Neurological disorders  BG: O- NA: Mr. Tessy RD: 17.05.2011 FA: 58.0 EID: cid003 GPS: 27.178057,-78.007789"}

EXCEED_NAME_LENGTH = {
    SMS: "cli009 .EID CID003 .NA Mr. O'brain .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
    RESPONSE_MESSAGE: "Error. Incorrect answer for question na. Please resend entire message."}

VALID_DATA2 = {SMS: "cli005 .EID cid004 .NA Mr. O'man .FA 58 .RD 17.05.2011 .BG b .SY ade .GPS 27.178057  -78.007789",
               RESPONSE_MESSAGE: "Thank you TEST. We received : EID: cid004 NA: Mr. O'man FA: 58.0 RD: 17.05.2011 BG: O- SY: Rapid weight loss,Memory loss,Neurological disorders  GPS: 27.178057,-78.007789"}

SMS_WITH_UNICODE = {
    SMS: u"cli005 .EID CID003 .NA Mr. O'brain .FA 58 .RD 17.05.2º11 .BG å .SY åde .GPS 27.178057º  -78.007789",
    RESPONSE_MESSAGE: "Error. Incorrect answer for question na, rd, bg, sy, gps. Please resend entire message."}

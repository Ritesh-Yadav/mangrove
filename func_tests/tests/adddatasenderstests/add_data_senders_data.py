# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
NAME = "name"
TELEPHONE_NUMBER = "telephone_number"
COMMUNE = "commune"
GPS = "gps"
SUCCESS_MSG = "message"
ERROR_MSG = "message"


BLANK_FIELDS = {NAME: "",
                TELEPHONE_NUMBER: "",
                COMMUNE: "",
                GPS: "",
                ERROR_MSG: "* Name This field is required.* Mobile Number This field is required.Enter location Please fill out at least one location field correctly.GPS: Enter Lat Long Please fill out at least one location field correctly."}

VALID_DATA = {NAME: "Mickey Duck",
              TELEPHONE_NUMBER: "9876543210",
              COMMUNE: "MAHAVELO, FIANARANTSOA",
              GPS: "48.955267  1.816013",
              SUCCESS_MSG: "Registration successful. Unique identification number\(ID\) is: rep"}

EXISTING_DATA = {NAME: "Mickey Mouse",
              TELEPHONE_NUMBER: "1234567890",
              COMMUNE: "MAHAVELO, FIANARANTSOA",
              GPS: "48.955267  1.816013",
              SUCCESS_MSG: "Sorry, the telephone number 1234567890 has already been registered"}

WITHOUT_LOCATION_NAME = {NAME: "Mini Mouse",
              TELEPHONE_NUMBER: "3456734568",
              COMMUNE: "",
              GPS: "23.955267  45.816013",
              SUCCESS_MSG: "Registration successful. Unique identification number\(ID\) is: rep"}

WITHOUT_GPS = {NAME: "Alladin",
              TELEPHONE_NUMBER: "4567345683",
              COMMUNE: "MAHAVELO",
              GPS: "",
              SUCCESS_MSG: "Registration successful. Unique identification number\(ID\) is: rep"}

INVALID_LATITUDE_GPS = {NAME: "Invalid Latitude GPS",
              TELEPHONE_NUMBER: "6734568345",
              COMMUNE: "",
              GPS: "123 90",
              SUCCESS_MSG: "GPS: Enter Lat Long Incorrect GPS format. The GPS coordinates must be in the following format: xx.xxxx yy.yyyy. Example -18.8665 47.5315"}

INVALID_LONGITUDE_GPS = {NAME: "Invalid Longitude GPS",
              TELEPHONE_NUMBER: "7345683456",
              COMMUNE: "",
              GPS: "23 190",
              SUCCESS_MSG: "GPS: Enter Lat Long Incorrect GPS format. The GPS coordinates must be in the following format: xx.xxxx yy.yyyy. Example -18.8665 47.5315"}

INVALID_GPS = {NAME: "Invalid GPS with Semi-Colon",
              TELEPHONE_NUMBER: "7345683456",
              COMMUNE: "",
              GPS: "23; 10",
              SUCCESS_MSG: "GPS: Enter Lat Long Incorrect GPS format. The GPS coordinates must be in the following format: xx.xxxx yy.yyyy. Example -18.8665 47.5315"}

INVALID_GPS_WITH_COMMA = {NAME: "Invalid GPS With Comma",
              TELEPHONE_NUMBER: "7345683456",
              COMMUNE: "",
              GPS: "23,10",
              SUCCESS_MSG: "GPS: Enter Lat Long Incorrect GPS format. The GPS coordinates must be in the following format: xx.xxxx yy.yyyy. Example -18.8665 47.5315"}


WITH_UNICODE_IN_GPS = {NAME: "Unicode in GPS",
              TELEPHONE_NUMBER: "5673456834",
              COMMUNE: "",
              GPS: "23º 45",
              SUCCESS_MSG: "GPS: Enter Lat Long Incorrect GPS format. The GPS coordinates must be in the following format: xx.xxxx yy.yyyy. Example -18.8665 47.5315"}

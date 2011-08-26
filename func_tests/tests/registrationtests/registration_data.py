# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

#Registration Page Test Data

##Variables
ORGANIZATION_NAME = 'organization_name'
ORGANIZATION_SECTOR = 'organization_sector'
ORGANIZATION_ADDRESS = 'organization_addressline'
ORGANIZATION_CITY = 'organization_city'
ORGANIZATION_STATE = 'organization_state'
ORGANIZATION_COUNTRY = 'organization_country'
ORGANIZATION_ZIPCODE = 'organization_zipcode'
ORGANIZATION_OFFICE_PHONE = 'organization_office_phone'
ORGANIZATION_WEBSITE = 'organization_website'
TITLE = 'title'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
EMAIL = 'email'
REGISTRATION_PASSWORD = 'registration_password'
REGISTRATION_CONFIRM_PASSWORD = 'registration_confirm_password'
SUCCESS_MESSAGE = 'message'
ERROR_MESSAGE = 'message'
ADMIN_OFFICE_NUMBER = "admin_office_number"
ADMIN_MOBILE_NUMBER = "admin_mobile_number"
ADMIN_SKYPE_ID = "admin_skype_id"

#Registration Page Data for Successful Registration Page
REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION = {ORGANIZATION_NAME: u"ÑGÓ 001",
                                                 ORGANIZATION_SECTOR: u"PublicHealth",
                                                 ORGANIZATION_ADDRESS: u"Address Line öne",
                                                 ORGANIZATION_CITY: u"Pünë",
                                                 ORGANIZATION_STATE: u"Máharashtra",
                                                 ORGANIZATION_COUNTRY: u"Indiá",
                                                 ORGANIZATION_ZIPCODE: u"411028",
                                                 ORGANIZATION_OFFICE_PHONE: u"0123456789",
                                                 ORGANIZATION_WEBSITE: u"http://ngo001.com",
                                                 TITLE: u"Mr",
                                                 FIRST_NAME: u"Nö",
                                                 LAST_NAME: u"Gö",
                                                 EMAIL: u"ngo",
                                                 ADMIN_MOBILE_NUMBER: "23-45-678-567",
                                                 ADMIN_OFFICE_NUMBER: "23-45-678-567",
                                                 ADMIN_SKYPE_ID: "tty01",
                                                 REGISTRATION_PASSWORD: u"ngo001",
                                                 REGISTRATION_CONFIRM_PASSWORD: u"ngo001",
                                                 SUCCESS_MESSAGE: u"You have successfully registered!!\nAn activation email has been sent to your email address. Please activate before login."}

EXISTING_EMAIL_ADDRESS = {ORGANIZATION_NAME: u"NGO 001",
                          ORGANIZATION_SECTOR: u"PublicHealth",
                          ORGANIZATION_ADDRESS: u"Address Line One",
                          ORGANIZATION_CITY: u"Pune",
                          ORGANIZATION_STATE: u"Maharashtra",
                          ORGANIZATION_COUNTRY: u"India",
                          ORGANIZATION_ZIPCODE: u"411028",
                          ORGANIZATION_OFFICE_PHONE: u"2345adbc234",
                          ORGANIZATION_WEBSITE: u"http://ngo001.com",
                          TITLE: u"Mr",
                          FIRST_NAME: u"No",
                          LAST_NAME: u"Go",
                          EMAIL: u"tester150411@gmail.com",
                          ADMIN_MOBILE_NUMBER: "2345adbc234",
                          ADMIN_OFFICE_NUMBER: "2345adbc234",
                          ADMIN_SKYPE_ID: "tty01",
                          REGISTRATION_PASSWORD: u"ngo001",
                          REGISTRATION_CONFIRM_PASSWORD: u"ngo001",
                          ERROR_MESSAGE: u"Office Phone Number Please enter a valid phone number* Email address This email address is already in use. Please supply a different email address.Office Phone Please enter a valid phone numberMobile Phone Please enter a valid phone number"}

INVALID_EMAIL_FORMAT = {ORGANIZATION_NAME: u"NGO 001",
                        ORGANIZATION_SECTOR: u"PublicHealth",
                        ORGANIZATION_ADDRESS: u"Address Line One",
                        ORGANIZATION_CITY: u"Pune",
                        ORGANIZATION_STATE: u"Maharashtra",
                        ORGANIZATION_COUNTRY: u"India",
                        ORGANIZATION_ZIPCODE: u"411028",
                        ORGANIZATION_OFFICE_PHONE: "+91678646792-67",
                        ORGANIZATION_WEBSITE: u"http://ngo001.com",
                        TITLE: u"Mr",
                        FIRST_NAME: u"No",
                        LAST_NAME: u"Go",
                        EMAIL: u"com.invalid@email",
                        ADMIN_MOBILE_NUMBER: "+91678646792-67",
                        ADMIN_OFFICE_NUMBER: "+91678-64679267",
                        ADMIN_SKYPE_ID: "tty01",
                        REGISTRATION_PASSWORD: u"ngo001",
                        REGISTRATION_CONFIRM_PASSWORD: u"ngo001",
                        ERROR_MESSAGE: u"Office Phone Number Please enter a valid phone number* Email address Enter a valid email address. Example:name@organization.comOffice Phone Please enter a valid phone numberMobile Phone Please enter a valid phone number"}

UNMATCHED_PASSWORD = {ORGANIZATION_NAME: u"NGO 001",
                      ORGANIZATION_SECTOR: u"PublicHealth",
                      ORGANIZATION_ADDRESS: u"Address Line One",
                      ORGANIZATION_CITY: u"Pune",
                      ORGANIZATION_STATE: u"Maharashtra",
                      ORGANIZATION_COUNTRY: u"India",
                      ORGANIZATION_ZIPCODE: u"411028",
                      ORGANIZATION_OFFICE_PHONE: u"(01)23456789",
                      ORGANIZATION_WEBSITE: u"http://ngo001.com",
                      TITLE: u"Mr",
                      FIRST_NAME: u"No",
                      LAST_NAME: u"Go",
                      EMAIL: u"valid@email.com",
                      ADMIN_MOBILE_NUMBER: "(91)678646792-67",
                      ADMIN_OFFICE_NUMBER: "(91)678-64679267",
                      ADMIN_SKYPE_ID: "tty01",
                      REGISTRATION_PASSWORD: u"password",
                      REGISTRATION_CONFIRM_PASSWORD: u"different_password",
                      ERROR_MESSAGE: u"Password The two password fields didn't match."}

WITHOUT_ENTERING_REQUIRED_FIELDS = {ORGANIZATION_NAME: u"",
                                    ORGANIZATION_SECTOR: u"PublicHealth",
                                    ORGANIZATION_ADDRESS: u"",
                                    ORGANIZATION_CITY: u"",
                                    ORGANIZATION_STATE: u"",
                                    ORGANIZATION_COUNTRY: u"",
                                    ORGANIZATION_ZIPCODE: u"",
                                    ORGANIZATION_OFFICE_PHONE: u"",
                                    ORGANIZATION_WEBSITE: u"",
                                    TITLE: u"",
                                    FIRST_NAME: u"",
                                    LAST_NAME: u"",
                                    EMAIL: u"",
                                    ADMIN_MOBILE_NUMBER: "",
                                    ADMIN_OFFICE_NUMBER: "",
                                    ADMIN_SKYPE_ID: "",
                                    REGISTRATION_PASSWORD: u"",
                                    REGISTRATION_CONFIRM_PASSWORD: u"",
                                    ERROR_MESSAGE: u"* Organization Name This field is required.* Address This field is required.* City This field is required.* Postal / Zip Code This field is required.* Country This field is required.* First name This field is required.* Last name This field is required.* Email address This field is required.Password This field is required.Password (again) This field is required."}

INVALID_WEBSITE_URL = {ORGANIZATION_NAME: u"NGO 001",
                       ORGANIZATION_SECTOR: u"PublicHealth",
                       ORGANIZATION_ADDRESS: u"Address Line One",
                       ORGANIZATION_CITY: u"Pune",
                       ORGANIZATION_STATE: u"Maharashtra",
                       ORGANIZATION_COUNTRY: u"India",
                       ORGANIZATION_ZIPCODE: u"411028",
                       ORGANIZATION_OFFICE_PHONE: u"1234AB56789",
                       ORGANIZATION_WEBSITE: u"ngo001",
                       TITLE: u"Mr",
                       FIRST_NAME: u"No",
                       LAST_NAME: u"Go",
                       EMAIL: u"ngo002@ngo.com",
                       ADMIN_MOBILE_NUMBER: "6786AB4679267",
                       ADMIN_OFFICE_NUMBER: "678CD64679267",
                       ADMIN_SKYPE_ID: "tty01",
                       REGISTRATION_PASSWORD: u"ngo001",
                       REGISTRATION_CONFIRM_PASSWORD: u"ngo001",
                       ERROR_MESSAGE: u"Office Phone Number Please enter a valid phone numberWebsite Url Enter a valid URL.Office Phone Please enter a valid phone numberMobile Phone Please enter a valid phone number"}

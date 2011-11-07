# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

#Registration Page Test Data

##Variables
from framework.utils.common_utils import by_css, by_xpath

ORGANIZATION_NAME = 'organization_name'
ORGANIZATION_SECTOR = 'organization_sector'
ORGANIZATION_ADDRESS = 'organization_address'
ORGANIZATION_CITY = 'organization_city'
ORGANIZATION_STATE = 'organization_state'
ORGANIZATION_COUNTRY = 'organization_country'
ORGANIZATION_ZIPCODE = 'organization_zipcode'
ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE = 'organization_office_phone_country_code'
ORGANIZATION_OFFICE_PHONE = 'organization_office_phone'
ORGANIZATION_WEBSITE = 'organization_website'
TITLE = 'title'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
EMAIL = 'email'
REGISTRATION_PASSWORD = 'password1'
REGISTRATION_CONFIRM_PASSWORD = 'password2'
WIRE_TRANSFER = 'wire_transfer'
PAY_MONTHLY = 'pay_monthly'
ERROR_MESSAGE = 'message'
ADMIN_OFFICE_NUMBER_COUNTRY_CODE = "office_phone_country_code"
ADMIN_OFFICE_NUMBER = "office_phone"
ADMIN_MOBILE_NUMBER_COUNTRY_CODE = "mobile_phone_country_code"
ADMIN_MOBILE_NUMBER = "mobile_phone"
ADMIN_SKYPE_ID = "skype"
ORGANIZATION_SECTOR_DROP_DOWN_LIST = by_css("select#id_organization_sector")
ORGANIZATION_OFFICE_PHONE_NUMBER_DROP_DOWN_LIST = by_css("select#id_office_phone_country_code")
ABOUT_DATAWINNERS_BOX = by_xpath('//div[@class="grid_7 right_hand_section alpha omega about_datawinners"')

#Registration Page Data for Successful Registration Page
REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION = {ORGANIZATION_NAME: u"ÑGÓ 001",
                                                 ORGANIZATION_SECTOR: u"PublicHealth",
                                                 ORGANIZATION_ADDRESS: u"Address Line öne",
                                                 ORGANIZATION_CITY: u"Pünë",
                                                 ORGANIZATION_STATE: u"Máharashtra",
                                                 ORGANIZATION_COUNTRY: u"Indiá",
                                                 ORGANIZATION_ZIPCODE: u"411028",
                                                 ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE: u"+86",
                                                 ORGANIZATION_OFFICE_PHONE: u"0123456789",
                                                 ORGANIZATION_WEBSITE: u"http://ngo001.com",
                                                 TITLE: u"Mr",
                                                 FIRST_NAME: u"Mickey",
                                                 LAST_NAME: u"Gö",
                                                 EMAIL: u"ngo",
                                                 ADMIN_MOBILE_NUMBER_COUNTRY_CODE: u"+86",
                                                 ADMIN_MOBILE_NUMBER: "23-45-678-567",
                                                 ADMIN_OFFICE_NUMBER_COUNTRY_CODE: u"+86",
                                                 ADMIN_OFFICE_NUMBER: "23-45-678-567",
                                                 ADMIN_SKYPE_ID: "tty01",
                                                 REGISTRATION_PASSWORD: u"ngo001",
                                                 REGISTRATION_CONFIRM_PASSWORD: u"ngo001",
                                                 PAY_MONTHLY: PAY_MONTHLY,
                                                 WIRE_TRANSFER: WIRE_TRANSFER}

REGISTRATION_SUCCESS_MESSAGE = u"You have successfully registered!!\nAn activation email has been sent to your email address. Please activate before login."

REGISTRATION_DATA_FOR_SUCCESSFUL_TRIAL_REGISTRATION = {ORGANIZATION_NAME: u"ÑGÓ 001",
                                                       ORGANIZATION_SECTOR: u"PublicHealth",
                                                       ORGANIZATION_CITY: u"Pünë",
                                                       ORGANIZATION_COUNTRY: u"Indiá",
                                                       FIRST_NAME: u"Nö",
                                                       LAST_NAME: u"Gö",
                                                       EMAIL: u"ngo",
                                                       REGISTRATION_PASSWORD: REGISTRATION_PASSWORD,
                                                       REGISTRATION_CONFIRM_PASSWORD: REGISTRATION_PASSWORD}

EXISTING_EMAIL_ADDRESS = {ORGANIZATION_NAME: u"NGO 001",
                          ORGANIZATION_SECTOR: u"PublicHealth",
                          ORGANIZATION_ADDRESS: u"Address Line One",
                          ORGANIZATION_CITY: u"Pune",
                          ORGANIZATION_STATE: u"Maharashtra",
                          ORGANIZATION_COUNTRY: u"India",
                          ORGANIZATION_ZIPCODE: u"411028",
                          ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE: u"+86",
                          ORGANIZATION_OFFICE_PHONE: u"2345234",
                          ORGANIZATION_WEBSITE: u"http://ngo001.com",
                          TITLE: u"Mr",
                          FIRST_NAME: u"No",
                          LAST_NAME: u"Go",
                          EMAIL: u"tester150411@gmail.com",
                          ADMIN_SKYPE_ID: "tty01",
                          REGISTRATION_PASSWORD: u"ngo001",
                          REGISTRATION_CONFIRM_PASSWORD: u"ngo001"}

EXISTING_EMAIL_ADDRESS_ERROR_MESSAGE = u"Email address This email address is already in use. Please supply a different email address."

UNMATCHED_PASSWORD = {ORGANIZATION_NAME: u"NGO 001",
                      ORGANIZATION_SECTOR: u"PublicHealth",
                      ORGANIZATION_ADDRESS: u"Address Line One",
                      ORGANIZATION_CITY: u"Pune",
                      ORGANIZATION_STATE: u"Maharashtra",
                      ORGANIZATION_COUNTRY: u"India",
                      ORGANIZATION_ZIPCODE: u"411028",
                      ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE: u"+86",
                      ORGANIZATION_OFFICE_PHONE: u"(01)23456789",
                      ORGANIZATION_WEBSITE: u"http://ngo001.com",
                      TITLE: u"Mr",
                      FIRST_NAME: u"No",
                      LAST_NAME: u"Go",
                      EMAIL: u"valid@email.com",
                      ADMIN_MOBILE_NUMBER_COUNTRY_CODE: u"+86",
                      ADMIN_MOBILE_NUMBER: u"(91)678646792-67",
                      ADMIN_OFFICE_NUMBER_COUNTRY_CODE: u"+86",
                      ADMIN_OFFICE_NUMBER: u"(91)678-64679267",
                      ADMIN_SKYPE_ID: "tty01",
                      REGISTRATION_PASSWORD: u"password",
                      REGISTRATION_CONFIRM_PASSWORD: u"different_password"}

UNMATCHED_PASSWORD_ERROR_MESSAGE = u"Password The two password fields didn't match."

WITHOUT_ENTERING_REQUIRED_FIELDS = {ORGANIZATION_NAME: u"",
                                    ORGANIZATION_SECTOR: u"PublicHealth",
                                    ORGANIZATION_ADDRESS: u"",
                                    ORGANIZATION_CITY: u"",
                                    ORGANIZATION_STATE: u"",
                                    ORGANIZATION_COUNTRY: u"",
                                    ORGANIZATION_ZIPCODE: u"",
                                    ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE: u"+86",
                                    ORGANIZATION_OFFICE_PHONE: u"",
                                    ORGANIZATION_WEBSITE: u"",
                                    TITLE: u"",
                                    FIRST_NAME: u"",
                                    LAST_NAME: u"",
                                    EMAIL: u"",
                                    ADMIN_MOBILE_NUMBER_COUNTRY_CODE: u"+86",
                                    ADMIN_MOBILE_NUMBER: u"",
                                    ADMIN_OFFICE_NUMBER_COUNTRY_CODE: u"+86",
                                    ADMIN_OFFICE_NUMBER: u"",
                                    ADMIN_SKYPE_ID: "",
                                    REGISTRATION_PASSWORD: u"",
                                    REGISTRATION_CONFIRM_PASSWORD: u""}

WITHOUT_PREFERRED_PAYMENT = {ORGANIZATION_NAME: u"ÑGÓ 001",
                             ORGANIZATION_SECTOR: u"PublicHealth",
                             ORGANIZATION_ADDRESS: u"Address Line öne",
                             ORGANIZATION_CITY: u"Pünë",
                             ORGANIZATION_STATE: u"Máharashtra",
                             ORGANIZATION_COUNTRY: u"Indiá",
                             ORGANIZATION_ZIPCODE: u"411028",
                             ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE: u"+86",
                             ORGANIZATION_OFFICE_PHONE: u"0123456789",
                             ORGANIZATION_WEBSITE: u"http://ngo001.com",
                             TITLE: u"Mr",
                             FIRST_NAME: u"Mickey",
                             LAST_NAME: u"Gö",
                             EMAIL: u"ngo",
                             ADMIN_MOBILE_NUMBER_COUNTRY_CODE: u"+86",
                             ADMIN_MOBILE_NUMBER: u"23-45-678-567",
                             ADMIN_OFFICE_NUMBER_COUNTRY_CODE: u"+86",
                             ADMIN_OFFICE_NUMBER: u"23-45-678-567",
                             ADMIN_SKYPE_ID: "tty01",
                             REGISTRATION_PASSWORD: u"ngo001",
                             REGISTRATION_CONFIRM_PASSWORD: u"ngo001",
                             PAY_MONTHLY: PAY_MONTHLY}

WITHOUT_ENTERING_REQUIRED_FIELDS_ERROR_MESSAGE = u"Organization Name This field is required.Address This field is required.City This field is required.Postal / Zip Code This field is required.Country This field is required.First name This field is required.Last name This field is required.Email address This field is required.Password This field is required.Password (again) This field is required."

INVALID_WEBSITE_URL = {ORGANIZATION_NAME: u"NGO 001",
                       ORGANIZATION_SECTOR: u"PublicHealth",
                       ORGANIZATION_ADDRESS: u"Address Line One",
                       ORGANIZATION_CITY: u"Pune",
                       ORGANIZATION_STATE: u"Maharashtra",
                       ORGANIZATION_COUNTRY: u"India",
                       ORGANIZATION_ZIPCODE: u"411028",
                       ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE: u"+86",
                       ORGANIZATION_OFFICE_PHONE: u"123456789",
                       ORGANIZATION_WEBSITE: u"ngo001",
                       TITLE: u"Mr",
                       FIRST_NAME: u"No",
                       LAST_NAME: u"Go",
                       EMAIL: u"ngo002@ngo.com",
                       ADMIN_MOBILE_NUMBER_COUNTRY_CODE: u"+86",
                       ADMIN_MOBILE_NUMBER: u"67864679267",
                       ADMIN_OFFICE_NUMBER_COUNTRY_CODE: u"+86",
                       ADMIN_OFFICE_NUMBER: u"67864679267",
                       ADMIN_SKYPE_ID: "tty01",
                       REGISTRATION_PASSWORD: u"ngo001",
                       REGISTRATION_CONFIRM_PASSWORD: u"ngo001"}
INVALID_WEBSITE_URL_ERROR_MESSAGE = u"Website Url Optional Enter a valid URL."

INVALID_PHONE_NUMBERS = {ORGANIZATION_NAME: u"NGO 001",
                         ORGANIZATION_SECTOR: u"PublicHealth",
                         ORGANIZATION_ADDRESS: u"Address Line One",
                         ORGANIZATION_CITY: u"Pune",
                         ORGANIZATION_STATE: u"Maharashtra",
                         ORGANIZATION_COUNTRY: u"India",
                         ORGANIZATION_ZIPCODE: u"411028",
                         ORGANIZATION_OFFICE_PHONE_COUNTRY_CODE: u"+86",
                         ORGANIZATION_OFFICE_PHONE: u"1234AB56789",
                         ORGANIZATION_WEBSITE: u"http://ngo001.com",
                         TITLE: u"Mr",
                         FIRST_NAME: u"No",
                         LAST_NAME: u"Go",
                         EMAIL: u"ngo003@ngo.com",
                         ADMIN_MOBILE_NUMBER_COUNTRY_CODE: u"+86",
                         ADMIN_MOBILE_NUMBER: u"6786AB4679267",
                         ADMIN_OFFICE_NUMBER_COUNTRY_CODE: u"+86",
                         ADMIN_OFFICE_NUMBER: u"678CD64679267",
                         ADMIN_SKYPE_ID: "tty01",
                         REGISTRATION_PASSWORD: u"ngo001",
                         REGISTRATION_CONFIRM_PASSWORD: u"ngo001"}
COUNTRY_CODE_TEXT = u"Select  Afghanistan +93 Albania +355 Algeria +213 American Samoa +1684 Andorra +376 Angola +244 Anguilla +1264 Antarctica +672 Antigua and Barbuda +1268 Argentina +54 Armenia +374 Aruba +297 Australia +61 Austria +43 Azerbaijan +994 Bahamas +1242 Bahrain +973 Bangladesh +880 Barbados +1246 Belarus +375 Belgium +32 Belize +501 Benin +229 Bermuda +1441 Bhutan +975 Bolivia +591 Bosnia and Herzegovina +387 Botswana +267 Brazil +55 Brunei +673 Bulgaria +359 Burkina Faso +226 Burundi +257 Cambodia +855 Cameroon +237 Canada +1 Cape Verde +238 Cayman Islands +1345 Central African Republic +236 Chad +235 Chile +56 China +86 Colombia +57 Comoros +269 Congo +242 Congo, The Democratic Republic of the +243 Cook Islands +682 Costa Rica +506 Cote D'Ivoire +225 Croatia +385 Cuba +53 Cyprus +357 Czech Republic +420 Denmark +45 Djibouti +253 Dominica +1767 Dominican Republic +18 Ecuador +593 Egypt +20 El Salvador +503 Equatorial Guinea +240 Eritrea +291 Estonia +372 Ethiopia +251 Falkland Islands (Malvinas) +500 Faroe Islands +298 Fiji +679 Finland +358 France +33 French Guiana +594 French Polynesia +689 Gabon +241 Gambia +220 Georgia +995 Germany +49 Ghana +233 Gibraltar +350 Greece +30 Greenland +299 Grenada +1473 Guadeloupe +590 Guam +1671 Guatemala +502 Guinea +224 Guinea-Bissau +245 Guyana +592 Haiti +509 Honduras +504 Hong Kong S.A.R., China +852 Hungary +36 Iceland +354 India +91 Indonesia +62 Iran +98 Iraq +964 Ireland +353 Israel +972 Italy +39 Jamaica +1876 Japan +81 Jordan +962 Kazakhstan +7 Kenya +254 Kiribati +686 Korea, North +850 Korea, South +82 Kuwait +965 Kyrgyzstan +996 Laos +856 Latvia +371 Lebanon +961 Lesotho +266 Liberia +231 Libya +218 Liechtenstein +423 Lithuania +370 Luxembourg +352 Macao +853 Macedonia +389 Madagascar +261 Malawi +265 Malaysia +60 Maldives +960 Mali +223 Malta +356 Marshall Islands +692 Martinique +596 Mauritania +222 Mauritius +230 Mayotte +269 Mexico +52 Micronesia, Federated States Of +691 Moldova +373 Monaco +377 Mongolia +976 Montenegro +382 Montserrat +1664 Morocco +212 Mozambique +258 Myanmar +95 Namibia +264 Nauru +674 Nepal +977 Netherlands +31 Netherlands Antilles +599 New Caledonia +687 New Zealand +64 Nicaragua +505 Niger +227 Nigeria +234 Niue +683 Northern Mariana Islands +1670 Norway +47 Oman +968 Pakistan +92 Palau +680 Panama +507 Papua New Guinea +675 Paraguay +595 Peru +51 Philippines +63 Poland +48 Portugal +351 Puerto Rico +1787 Qatar +974 Reunion +262 Romania +40 Russia +7 Rwanda +250 Saint Helena +290 Saint Kitts and Nevis +1869 Saint Lucia +1758 Saint Pierre and Miquelon +508 Saint Vincent and the Grenadines +1784 Samoa +685 San Marino +378 Sao Tome and Principe +239 Saudi Arabia +966 Senegal +221 Serbia +381 Seychelles +248 Sierra Leone +232 Singapore +65 Slovakia +421 Slovenia +386 Solomon Islands +677 Somalia +252 South Africa +27 Spain +34 Sri Lanka +94 Sudan +249 Suriname +597 Swaziland +268 Sweden +46 Switzerland +41 Syria +963 Taiwan +886 Tajikistan +992 Tanzania +255 Thailand +66 Timor-Leste +670 Togo +228 Tokelau +690 Tonga +676 Trinidad and Tobago +1868 Tunisia +216 Turkey +90 Turkmenistan +993 Turks and Caicos Islands +1649 Tuvalu +688 Uganda +256 Ukraine +380 United Arab Emirates +971 United Kingdom +44 United States +1 Uruguay +598 Uzbekistan +998 Vanuatu +678 Vatican City State (Holy See) +3 Venezuela +58 Vietnam +84 Virgin Islands, British +1284 Virgin Islands, US +1340 Wallis and Futuna +681 Yemen +967 Zambia +260 Zimbabwe +263 "
INVALID_PHONE_NUMBERS_ERROR_MESSAGE = u"Office Phone Number Optional " + COUNTRY_CODE_TEXT + "Please enter a valid phone number.Office Phone Optional " + COUNTRY_CODE_TEXT + "Please enter a valid phone number.Mobile Phone Optional " + COUNTRY_CODE_TEXT + "Please enter a valid phone number."

PHONE_NUMBERS_WITHOUT_COUNTRY_CODE = {ORGANIZATION_NAME: u"NGO 001",
                                      ORGANIZATION_SECTOR: u"PublicHealth",
                                      ORGANIZATION_ADDRESS: u"Address Line One",
                                      ORGANIZATION_CITY: u"Pune",
                                      ORGANIZATION_STATE: u"Maharashtra",
                                      ORGANIZATION_COUNTRY: u"India",
                                      ORGANIZATION_ZIPCODE: u"411028",
                                      ORGANIZATION_OFFICE_PHONE: u"425826677",
                                      ORGANIZATION_WEBSITE: u"http://ngo001.com",
                                      TITLE: u"Mr",
                                      FIRST_NAME: u"No",
                                      LAST_NAME: u"Go",
                                      EMAIL: u"ngo004@ngo.com",
                                      ADMIN_MOBILE_NUMBER: u"425826677",
                                      ADMIN_OFFICE_NUMBER: u"425826677",
                                      ADMIN_SKYPE_ID: "tty01",
                                      REGISTRATION_PASSWORD: u"ngo001",
                                      REGISTRATION_CONFIRM_PASSWORD: u"ngo001"}

PHONE_NUMBERS_WITHOUT_COUNTRY_CODE_ERROR_MESSAGE = u"Office Phone Number Optional " + COUNTRY_CODE_TEXT + "Please enter a country code.Office Phone Optional " + COUNTRY_CODE_TEXT + "Please enter a country code.Mobile Phone Optional " + COUNTRY_CODE_TEXT + "Please enter a country code."

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

PROJECT_NAME = "project_name"
QUESTIONS = "questions"
DATA_RECORDS = "data_records"
DATE_RANGE = "date_range"
CURRENT_MONTH = "current_month"
LAST_MONTH = "last_month"
YEAR_TO_DATE = "year_to_date"

DEFAULT_DATA_FOR_QUESTIONNAIRE = {PROJECT_NAME: "clinic test project",
                      QUESTIONS: [u'What is your namé?',
                                  u'What is age öf father?',
                                  u'What is réporting date?',
                                  u'What is your blood group?',
                                  u'What aré symptoms?',
                                  u'What is the GPS codé for clinic',
                                  u'What are the required medicines?'],
                      DATA_RECORDS: [u'cid001 ànita 45 07.03.2011 O- Dry cough,Neurological disorders 45.233,28.3324 --',
                                    u'cid002 Amanda 62 12.03.2011 AB Dry cough,Memory loss 40.2,69.3123 --',
                                    u'cid003 Jimanda 80 12.03.2011 AB Dry cough,Memory loss 40.2,69.3123 --',
                                    u'cid004 ànnita 30 07.03.2011 O- Dry cough,Neurological disorders 45.233,28.3324 --',
                                    u'cid005 Qamanda 50 12.03.2011 AB Dry cough,Memory loss 40.2,69.3123 --',
                                    u'cid007 Amanda -- 12.11.2010 AB Dry cough,Memory loss 40.2,69.3123 --',
                                    u'cli10 Zorro 43 05.05.2011 O- Pneumonia,Memory loss 23.23452,-28.3456 --',
                                    u'cli11 Aàntra 91 12.05.2011 O+ Dry cough,Rapid weight loss -45.234,89.32345 --',
                                    u'cli12 ànnita 45 15.05.2010 B+ Pneumonia,Dry cough,Neurological disorders -78.233,-28.3324 --',
                                    u'cli13 Dmanda 89 04.06.2011 AB Pneumonia,Neurological disorders 40.2,69.3123 --']}

FILTER_BY_CURRENT_MONTH = {PROJECT_NAME: "clinic test project",
                           DATE_RANGE: CURRENT_MONTH,
                           DATA_RECORDS: [u'cli13 Dmanda 89 04.06.2011 AB Pneumonia,Neurological disorders 40.2,69.3123 --',
                                          u'cli14 Vamand 56 01.06.2011 O+ Rapid weight loss,Pneumonia,Neurological disorders 58.3452,115.3345 --',
                                          u'cli15 M!lo 45 07.06.2011 -- Dry cough,Rapid weight loss 19.672,92.33456 --',
                                          u'cli16 K!llo 28 -- -- -- 19.672,92.33456 --',
                                          u'cli17 Catty 98 25.06.2011 O- Memory loss,Pneumonia,Neurological disorders 33.23452,-68.3456 --',
                                          u'cli18 àntra 58 22.06.2011 O+ Rapid weight loss,Memory loss,Dry cough -45.234,169.32345 --',
                                          u'cli9 Tinnita 27 -- B+ Rapid weight loss,Pneumonia,Neurological disorders -78.233,-28.3324 --']}

FILTER_BY_LAST_MONTH = {PROJECT_NAME: "clinic test project",
                           DATE_RANGE: LAST_MONTH,
                           DATA_RECORDS: [u'cli10 Zorro 43 05.05.2011 O- Pneumonia,Memory loss 23.23452,-28.3456 --',
                                          u'cli11 Aàntra 91 12.05.2011 O+ -- -45.234,89.32345 --',
                                          u'cli12 ànnita 45 15.05.2010 B+ Pneumonia,Dry cough,Neurological disorders -78.233,-28.3324 --',
                                          u'cli9 Demelo 32 27.05.2011 AB Dry cough,Rapid weight loss 19.672,92.33456 --']}

FILTER_BY_YEAR_TO_DATE = {PROJECT_NAME: "clinic test project",
                          DATE_RANGE: YEAR_TO_DATE,
                          DATA_RECORDS: [
                              u'cid001 ànita 45 07.03.2011 O- Dry cough,Neurological disorders 45.233,28.3324 --',
                              u'cid002 Amanda 62 12.03.2011 AB Dry cough,Memory loss 40.2,69.3123 --',
                              u'cid003 Jimanda 80 12.03.2011 AB Dry cough,Memory loss 40.2,69.3123 --',
                              u'cid004 ànnita 30 07.03.2011 O- Dry cough,Neurological disorders 45.233,28.3324 --',
                              u'cid005 Qamanda 50 12.03.2011 AB Dry cough,Memory loss 40.2,69.3123 --',
                              u'cli10 Zorro 43 05.05.2011 O- Pneumonia,Memory loss 23.23452,-28.3456 --',
                              u'cli11 Aàntra 91 12.05.2011 O+ -- -45.234,89.32345 --',
                              u'cli12 ànnita 45 15.05.2010 B+ Pneumonia,Dry cough,Neurological disorders -78.233,-28.3324 --',
                              u'cli13 Dmanda 89 04.06.2011 AB Pneumonia,Neurological disorders 40.2,69.3123 --',
                              u'cli14 Vamand 56 01.06.2011 O+ Rapid weight loss,Pneumonia,Neurological disorders 58.3452,115.3345 --',
                              u'cli15 M!lo 45 07.06.2011 -- Dry cough,Rapid weight loss 19.672,92.33456 --',
                              u'cli16 K!llo 28 -- -- -- 19.672,92.33456 --',
                              u'cli17 Catty 98 25.06.2011 O- Memory loss,Pneumonia,Neurological disorders 33.23452,-68.3456 --',
                              u'cli18 àntra 58 22.06.2011 O+ Rapid weight loss,Memory loss,Dry cough -45.234,169.32345 --',
                              u'cli9 Tinnita 27 27.05.2011 B+ Rapid weight loss,Pneumonia,Neurological disorders -78.233,-28.3324 --']}
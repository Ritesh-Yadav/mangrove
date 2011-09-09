-----------------------
Mangrove Tutorial
-----------------------

Introduction
------------
Follow the below steps to create a questionnaire form and submit data for the same:

*   **Create a Form**

    default_ddtype = DataDictType(self.dbm, name='Default String Datadict Type', slug='string_default',
                                           primitive_type='string')
    default_ddtype.save()
    question1 = TextField(name="Q1", code="ID", label="What is the reporter ID?",
                                  language="eng", entity_question_flag=True, ddtype=default_ddtype)

    question2 = TextField(name="Q2", code="DATE", label="What month and year are you reporting for?",
                                      language="eng", entity_question_flag=False, ddtype=default_ddtype)

    question3 = TextField(name="Q3", code="NETS", label="How many mosquito nets did you distribute?",
                                      language="eng", entity_question_flag=False, ddtype=default_ddtype)

    form_model = FormModel(dbm, entity_type=["Reporter"], name="Mosquito Net Distribution Survey",
                                    label="Mosquito Net Distribution Survey",
                                    form_code="MNET",
                                    type='survey',
                                    fields=[question1, question2, question3])
    form_model.save()

*   **Submit data to the form directly**

    values = { "ID" : "rep45", "DATE" : "10.2010", "NETS" : "50" }
    form = get_form_model_by_code(dbm, "MNET")
    form_submission = form.submit(dbm, values, submission_id)

*   **Submit data to the player**
    text = "MNET .ID rep45 .DATE 10.2010 .NETS 50"
    transport_info = TransportInfo(transport="sms", source="9923712345", destination="5678")
    sms_player = SMSPlayer(dbm)
    response = sms_player.accept(Request(transportInfo=transport_info, message=text))

    The player will also log the submission for you in Mangrove.

*   **Load all submissions for the form**

    get_submissions_made_for_form()

*   **Perform aggregations for the form**
    <code sample>
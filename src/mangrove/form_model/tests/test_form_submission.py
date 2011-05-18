# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from unittest.case import TestCase
from mock import Mock
from mangrove.datastore.database import DatabaseManager
from mangrove.datastore.datadict import DataDictType
from mangrove.errors.MangroveException import EntityQuestionCodeNotSubmitted
from mangrove.form_model.field import TextField, IntegerField, SelectField
from mangrove.form_model.form_model import FormModel, FormSubmission
from mangrove.form_model.validation import NumericConstraint


class TestFormSubmission(TestCase):
    def setUp(self):

        self.dbm = Mock(spec=DatabaseManager)
        self.ddtype1 = Mock(spec=DataDictType)
        self.ddtype2 = Mock(spec=DataDictType)
        self.ddtype3 = Mock(spec=DataDictType)
        self.ddtype4 = Mock(spec=DataDictType)

        question1 = TextField(name="entity_question", question_code="ID", label="What is associated entity",
                              language="eng", entity_question_flag=True, ddtype=self.ddtype1)
        question2 = TextField(name="Name", question_code="Q1", label="What is your name",
                              defaultValue="some default value", language="eng", ddtype=self.ddtype2)
        question3 = IntegerField(name="Father's age", question_code="Q2", label="What is your Father's Age",
                                 range=NumericConstraint(min=15, max=120), ddtype=self.ddtype3)
        question4 = SelectField(name="Color", question_code="Q3", label="What is your favourite color",
                                options=[("RED", 1), ("YELLOW", 2)], ddtype=self.ddtype4)

        self.form_model = FormModel(self.dbm, entity_type=["Clinic"], name="aids", label="Aids form_model",
                                    form_code="AIDS", type='survey',
                                    fields=[question1, question2, question3, question4])

    def tearDown(self):
        pass

    def test_should_create_form_submission_with_entity_id(self):
        answers = {"ID": "1", "Q1": "My Name", "Q2": "40", "Q3": "RED"}

        form_submission = FormSubmission(self.form_model, answers)

        self.assertEqual(form_submission.form_code, "AIDS")
        self.assertEqual(form_submission.short_code, "1")

    def test_should_create_form_submission_with_answer_values(self):
        answers = {"ID": "1", "Q1": "My Name", "Q2": "40", "Q3": "a"}

        form_submission = FormSubmission(self.form_model, answers)
        form_submission.is_valid()

        self.assertEqual(form_submission.cleaned_data, {"Name": "My Name", "Father's age": 40, "Color": ["RED"]})
        self.assertEqual(3, len(form_submission.values))
        self.assertIn(("Name", "My Name", self.ddtype2), form_submission.values)
        self.assertIn(("Father's age", 40, self.ddtype3), form_submission.values)
        self.assertIn(("Color", ["RED"], self.ddtype4), form_submission.values)

    def test_should_ignore_non_form_fields(self):
        answers = {"ID": "1", "Q1": "My Name", "Q2": "40", "Q3": "a", "EXTRA_FIELD": "X", "EXTRA_FIELD2": "Y"}

        f = FormSubmission(self.form_model, answers)
        f.is_valid()
        self.assertEqual({"Name": "My Name", "Father's age": 40, "Color": ["RED"]}, f.cleaned_data)
        self.assertEqual(3, len(f.values))
        self.assertIn(("Name", "My Name", self.ddtype2), f.values)
        self.assertIn(("Father's age", 40, self.ddtype3), f.values)
        self.assertIn(("Color", ["RED"], self.ddtype4), f.values)

    def test_should_ignore_fields_without_values(self):
        answers = {"ID": "1", "Q1": "My Name", "Q2": "", "Q3": "   "}
        f = FormSubmission(self.form_model, answers)
        self.assertTrue(f.is_valid())
        self.assertEqual(0, len(f.errors))
        self.assertEqual({"Name": "My Name"}, f.cleaned_data)
        self.assertEqual(1, len(f.cleaned_data))

    #    def test_should_strip_whitespaces(self):
    #        answers = {"ID": "1", "Q1": "   My Name", "Q2": "  40 ", "Q3": "RED     "}
    #        f = FormSubmission(self.form_model, answers)
    #        self.assertTrue(f.is_valid())
    #        self.assertEqual(0, len(f.errors))
    #        self.assertEqual({"Name": "My Name", "Father's age": 40, "Color": "RED"}, f.answers)
    #        self.assertEqual(3, len(f.values))

    #        Write negative scenarios
    #        Write is_valid scenarios
    def test_give_error_for_wrong_integer_answers(self):
        dbm = Mock(spec=DatabaseManager)
        question1 = TextField(name="entity_question", question_code="ID", label="What is associated entity", language="eng", entity_question_flag=True, ddtype=self.ddtype2)
        question3 = IntegerField(name="Father's age", question_code="Q2", label="What is your Father's Age",
                                 range=NumericConstraint(min=15, max=120), ddtype=self.ddtype3)

        form_model = FormModel(dbm, entity_type=["Clinic"], name="aids", label="Aids form_model",
                               form_code="AIDS", type='survey',
                               fields=[question1, question3])

        answers = {"ID": "1", "Q2": "10"}

        form_submission = FormSubmission(form_model, answers)
        self.assertFalse(form_submission.is_valid())
        self.assertEqual(len(form_submission.errors), 1)

    def test_give_error_for_no_entity_short_code(self):
        with self.assertRaises(EntityQuestionCodeNotSubmitted):
            dbm = Mock(spec=DatabaseManager)
            question1 = TextField(name="entity_question", question_code="ID", label="What is associated entity", language="eng", entity_question_flag=True, ddtype=self.ddtype2)
            question3 = IntegerField(name="Father's age", question_code="Q2", label="What is your Father's Age", ddtype=self.ddtype3)

            form_model = FormModel(dbm, entity_type=["Clinic"], name="aids", label="Aids form_model",
                                   form_code="AIDS", type='survey',
                                   fields=[question1, question3])
            answers = {"Q2": "10"}
            form_submission = FormSubmission(form_model, answers)
            form_submission.is_valid()


    def test_give_error_for_no_entity_short_code_while_registration(self):
        with self.assertRaises(EntityQuestionCodeNotSubmitted):
            dbm = Mock(spec=DatabaseManager)
            question1 = TextField(name="entity_question", question_code="ID", label="What is associated entity", language="eng", entity_question_flag=True, ddtype=self.ddtype2)
            question3 = IntegerField(name="Father's age", question_code="Q2", label="What is your Father's Age", ddtype=self.ddtype3)

            form_model = FormModel(dbm, entity_type=["Clinic"], name="aids", label="Aids form_model",
                                   form_code="AIDS", type='survey',
                                   fields=[question1, question3])
            answers = {"Q2": "10"}
            form_submission = FormSubmission(form_model, answers)
            form_submission.is_valid()


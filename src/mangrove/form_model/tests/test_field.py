# vim= ai ts=4 sts=4 et sw=4 encoding=utf-8

import unittest
from mock import Mock, patch
from mangrove.datastore.database import DatabaseManager
from mangrove.datastore.datadict import DataDictType

from mangrove.errors.MangroveException import IncorrectDate
from mangrove.form_model.field import DateField, LocationField

from mangrove.errors.MangroveException import AnswerTooBigException, AnswerTooSmallException,\
    AnswerTooLongException, AnswerTooShortException, AnswerWrongType, AnswerHasTooManyValuesException
from mangrove.form_model.field import TextField, IntegerField, SelectField

from mangrove.form_model import field
from mangrove.form_model.validation import NumericConstraint, TextConstraint


class TestField(unittest.TestCase):
    def setUp(self):
        self.ddtype = Mock(spec=DataDictType)
        self.DDTYPE_JSON = {'test': 'test'}
        self.ddtype.to_json.return_value = self.DDTYPE_JSON
        self.patcher = patch(target='mangrove.form_model.field.DataDictType', spec=DataDictType)
        self.ddtype_module = self.patcher.start()
        self.dbm = Mock(spec=DatabaseManager)

    def tearDown(self):
        self.patcher.stop()

    def test_should_create_text_field_type_for_default_english_language(self):
        expected_json = {
            "defaultValue": "some default value",
            "label": {"eng": "What is your name"},
            "name": "field1_Name",
            "code": "Q1",
            "length": {"min": 1, "max": 20},
            "type": "text",
            "ddtype": self.DDTYPE_JSON,
            }
        field = TextField(name="field1_Name", code="Q1", label="What is your name",
                             defaultValue="some default value", length=TextConstraint(1, 20), language="eng",
                             ddtype=self.ddtype)
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_create_integer_field_type_for_default_english_language(self):
        expected_json = {
            "label": {"eng": "What is your age"},
            "name": "Age",
            "code": "Q2",
            "range": {},
            "ddtype": self.DDTYPE_JSON,
            "type": "integer",
            }
        field = IntegerField(name="Age", code="Q2", label="What is your age",
                                language="eng", ddtype=self.ddtype)
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_create_integer_field_type_for_default_english_language_with_range(self):
        expected_json = {
            "label": {"eng": "What is your age"},
            "name": "Age",
            "code": "Q2",
            "range": {"min": 15, "max": 120},
            "ddtype": self.DDTYPE_JSON,
            "type": "integer",
            }
        field = IntegerField(name="Age", code="Q2", label="What is your age",
                                language="eng", range=NumericConstraint(min=15, max=120), ddtype=self.ddtype)
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_create_select_one_field_type_for_default_english_language(self):
        expected_json = {
            "label": {"eng": "What is your favorite color"},
            "name": "color",
            "choices": [{"text": {"eng": "RED"}, "val": 1}, {"text": {"eng": "YELLOW"}, "val": 2},
                        {"text": {'eng': 'green'}, "val": 3}],
            "code": "Q3",
            "ddtype": self.DDTYPE_JSON,
            "type": "select1",
            }
        field = SelectField(name="color", code="Q3", label="What is your favorite color",
                               language="eng", options=[("RED", 1), ("YELLOW", 2), ('green', 3)], ddtype=self.ddtype)
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_create_multi_select_field_type_for_default_english_language(self):
        expected_json = {
            "label": {"eng": "What is your favorite color"},
            "name": "color",
            "choices": [{"text": {"eng": "RED"}, "val": 1}, {"text": {"eng": "YELLOW"}, "val": 2},
                        {"text": {'eng': 'green'}}],
            "code": "Q3",
            "ddtype": self.DDTYPE_JSON,
            "type": "select",
            }
        field = SelectField(name="color", code="Q3", label="What is your favorite color",
                               language="eng", options=[("RED", 1), ("YELLOW", 2), ('green')], single_select_flag=False,
                               ddtype=self.ddtype)
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_add_label_for_french_language(self):
        expected_json = {
            "defaultValue": "some default value",
            "label": {"eng": "What is your name", "fra": "french label"},
            "name": "field1_Name",
            "code": "Q1",
            "length": {},
            "ddtype": self.DDTYPE_JSON,
            "type": "text"
        }
        field = TextField(name="field1_Name", code="Q1", label="What is your name",
                             defaultValue="some default value", ddtype=self.ddtype)
        field.add_or_edit_label(language="fra", label="french label")
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_edit_label_for_english_language(self):
        expected_json = {
            "defaultValue": "some default value",
            "label": {"eng": "english label", "fra": "french label"},
            "name": "field1_Name",
            "code": "Q1",
            "length": {},
            "ddtype": self.DDTYPE_JSON,
            "type": "text"
        }
        field = TextField(name="field1_Name", code="Q1", label="What is your name",
                             defaultValue="some default value", ddtype=self.ddtype)
        field.add_or_edit_label(language="fra", label="french label")
        field.add_or_edit_label(label="english label")
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_add_entity_field(self):
        expected_json = {
            "defaultValue": "",
            "label": {"eng": "What is your name"},
            "name": "field1_Name",
            "code": "Q1",
            "length": {},
            "type": "text",
            "ddtype": self.DDTYPE_JSON,
            "entity_question_flag": True
        }
        field = TextField(name="field1_Name", code="Q1", label="What is your name",
                             entity_question_flag=True, ddtype=self.ddtype)
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_create_text_field_from_dictionary(self):
        self.ddtype_module.create_from_json.return_value = self.ddtype
        field_json = {
            "defaultValue": "",
            "label": {"eng": "What is your name"},
            "name": "field1_Name",
            "code": "Q1",
            "type": "text",
            "length": {"min": 1, "max": 10},
            "entity_field_flag": True,
            "ddtype": self.ddtype
        }
        created_field = field.create_question_from(field_json, self.dbm)
        self.assertIsInstance(created_field, TextField)
        self.assertIsInstance(created_field.constraint, TextConstraint)
        self.assertEqual(created_field.constraint.max, 10)
        self.assertEqual(created_field.constraint.min, 1)
        self.assertEqual(created_field.ddtype, self.ddtype)

    def test_should_create_integer_field_with_validations(self):
        self.ddtype_module.create_from_json.return_value = self.ddtype
        field_json = {
            "defaultValue": "",
            "label": {"eng": "What is your age"},
            "name": "field1_age",
            "code": "Q1",
            "type": "integer",
            "ddtype": self.DDTYPE_JSON,
            "range": {"min": 0, "max": 100},
            "entity_field_flag": False
        }
        created_field = field.create_question_from(field_json, self.dbm)
        self.assertIsInstance(created_field, IntegerField)
        self.assertEqual(created_field._dict["range"], {"min": 0, "max": 100})
        self.assertIsInstance(created_field.constraint, NumericConstraint)
        self.assertEqual(created_field.constraint.max, 100)
        self.assertEqual(created_field.constraint.min, 0)
        self.assertEqual(created_field.ddtype, self.ddtype)

    def test_should_create_select_field_with_options(self):
        self.ddtype_module.create_from_json.return_value = self.ddtype
        field_json = {
            "name": "q3",
            "code": "qc3",
            "type": "select",
            "ddtype": self.DDTYPE_JSON,
            "choices": [{"text": {"eng": "option 1"}, "value": "c1"},
                        {"text": {"eng": "option 1"}, "value": "c2"}],
            "entity_field_flag": False}
        created_field = field.create_question_from(field_json, self.dbm)
        self.assertIsInstance(created_field, SelectField)
        self.assertEqual(created_field.SINGLE_SELECT_FLAG, False)
        self.assertEqual(created_field.ddtype, self.ddtype)


    def test_should_create_select_field_with_single_select_options(self):
        self.ddtype_module.create_from_json.return_value = self.ddtype
        field_json = {
            "name": "q3",
            "code": "qc3",
            "type": "select1",
            "ddtype": self.DDTYPE_JSON,
            "choices": [{"text": {"eng": "hello", "fr": "bonjour"}, "value": "c1"},
                        {"text": {"eng": "world"}, "value": "c2"}],
            "entity_field_flag": False}

        expected_option_list = [{"text": {"eng": "hello", "fr": "bonjour"}, "value": "c1"},
                                {"text": {"eng": "world"}, "value": "c2"}]
        created_field = field.create_question_from(field_json, self.dbm)
        self.assertIsInstance(created_field, SelectField)
        self.assertEqual(created_field.SINGLE_SELECT_FLAG, True)
        self.assertEqual(created_field.options, expected_option_list)
        self.assertEqual(created_field.ddtype, self.ddtype)

    def test_should_return_error_for_integer_range_validation(self):
        field = IntegerField(name="Age", code="Q2", label="What is your age",
                                language="eng", range=NumericConstraint(min=15, max=120), ddtype=self.ddtype)
        valid_value = field.validate("120")
        self.assertEqual(valid_value, 120)
        valid_value = field.validate("25.5")
        self.assertEqual(valid_value, 25.5)

    def test_should_return_error_for_wrong_type_for_integer(self):
        with self.assertRaises(AnswerWrongType) as e:
            field = IntegerField(name="Age", code="Q2", label="What is your age",
                                    language="eng", range=NumericConstraint(min=15, max=120), ddtype=self.ddtype)
            field.validate("asas")
        self.assertEqual(e.exception.message, "Answer to question Q2 is of wrong type.")

    def test_should_return_error_for_integer_range_validation_for_max_value(self):
        with self.assertRaises(AnswerTooBigException) as e:
            field = IntegerField(name="Age", code="Q2", label="What is your age",
                                    language="eng", range=NumericConstraint(min=15, max=120), ddtype=self.ddtype)
            valid_value = field.validate(150)
            self.assertFalse(valid_value)
        self.assertEqual(e.exception.message, "Answer 150 for question Q2 is greater than allowed.")

    def test_should_return_error_for_integer_range_validation_for_min_value(self):
        with self.assertRaises(AnswerTooSmallException) as e:
            field = IntegerField(name="Age", code="Q2", label="What is your age",
                                    language="eng", range=NumericConstraint(min=15, max=120), ddtype=self.ddtype)
            valid_value = field.validate(11)
            self.assertFalse(valid_value)
        self.assertEqual(e.exception.message, "Answer 11 for question Q2 is smaller than allowed.")

    def test_successful_text_length_validation(self):
        field = TextField(name="Name", code="Q2", label="What is your Name",
                             language="eng", length=TextConstraint(min=4, max=15), ddtype=self.ddtype)
        field1 = TextField(name="Name", code="Q2", label="What is your Name",
                              language="eng", ddtype=self.ddtype)
        valid_value = field.validate("valid")
        self.assertEqual(valid_value, "valid")
        valid_value = field1.validate("valid")
        self.assertEqual(valid_value, "valid")

    def test_should_return_error_for_text_length_validation_for_max_value(self):
        with self.assertRaises(AnswerTooLongException) as e:
            field = TextField(name="Age", code="Q2", label="What is your age",
                                 language="eng", length=TextConstraint(min=1, max=4), ddtype=self.ddtype)
            valid_value = field.validate("long_answer")
            self.assertFalse(valid_value)
        self.assertEqual(e.exception.message, "Answer long_answer for question Q2 is longer than allowed.")

    def test_should_return_error_for_text_length_validation_for_min_value(self):
        with self.assertRaises(AnswerTooShortException) as e:
            field = TextField(name="Age", code="Q2", label="What is your age",
                                 language="eng", length=TextConstraint(min=15, max=120), ddtype=self.ddtype)
            valid_value = field.validate("short")
            self.assertFalse(valid_value)
        self.assertEqual(e.exception.message, "Answer short for question Q2 is shorter than allowed.")

    def test_should_create_date_field(self):
        self.ddtype_module.create_from_json.return_value = self.ddtype
        field_json = {
            "defaultValue": "",
            "label": {"eng": "What is your birth date"},
            "name": "Birth_date",
            "code": "Q1",
            "type": "date",
            "date_format": "%m.%Y",
            "ddtype": self.DDTYPE_JSON,
            }
        created_field = field.create_question_from(field_json, self.dbm)
        self.assertIsInstance(created_field, DateField)
        self.assertEqual(created_field.date_format, "%m.%Y")
        self.assertEqual(created_field.ddtype, self.ddtype)

    def test_should_return_error_for_incorrect_date_format_error_for_wrong_format(self):
        with self.assertRaises(IncorrectDate) as e:
            field = DateField(name="Age", code="Q2", label="What is your birth date",
                                 language="eng", date_format="mm.yyyy", ddtype=self.ddtype)
            valid_value = field.validate("13.2010")
            self.assertFalse(valid_value)
        self.assertEqual(e.exception.message,
                         "Answer to question Q2 is invalid: 13.2010, expected date in mm.yyyy format")

        with self.assertRaises(IncorrectDate) as e:
            field = DateField(name="Age", code="Q2", label="What is your birth date",
                                 language="eng", date_format="dd.mm.yyyy", ddtype=self.ddtype)
            valid_value = field.validate("33.12.2010")
            self.assertFalse(valid_value)
        self.assertEqual(e.exception.message,
                         "Answer to question Q2 is invalid: 33.12.2010, expected date in dd.mm.yyyy format")

        with self.assertRaises(IncorrectDate) as e:
            field = DateField(name="Age", code="Q2", label="What is your birth date",
                                 language="eng", date_format="mm.dd.yyyy", ddtype=self.ddtype)
            valid_value = field.validate("13.01.2010")
            self.assertFalse(valid_value)
        self.assertEqual(e.exception.message,
                         "Answer to question Q2 is invalid: 13.01.2010, expected date in mm.dd.yyyy format")

    def test_should_validate_single_answer(self):
        with self.assertRaises(AnswerHasTooManyValuesException) as e:
            clinic_field = SelectField(name="clinic type", code="Q1", label="What type of clinic is it?",
                                          language="eng", options=["village", "urban"], single_select_flag=True,
                                          ddtype=self.ddtype)
            clinic_field.validate("vu")
        self.assertEqual(e.exception.message, "Answer vu for question Q1 contains more than one value.")


    def test_should_create_field_with_datadict_type(self):
        nameType = Mock(spec=DataDictType)
        field1 = TextField(name="Name", code="Q1", label="What is your Name",
                              language="eng", length=TextConstraint(min=4, max=15), ddtype=nameType)
        self.assertEqual(nameType, field1.ddtype)

        ageType = Mock(spec=DataDictType)
        field2 = IntegerField(name="Age", code="Q2", label="What is your age",
                                 language="eng", range=NumericConstraint(min=4, max=15), ddtype=ageType)
        self.assertEqual(ageType, field2.ddtype)

        selectType = Mock(spec=DataDictType)
        field3 = SelectField(name="clinic type", code="Q1", label="What type of clinic is it?",
                                language="eng", options=["village", "urban"], ddtype=selectType)

        self.assertEqual(selectType, field3.ddtype)

        dateType = Mock(spec=DataDictType)
        field4 = DateField(name="Age", code="Q2", label="What is your birth date",
                              language="eng", date_format="%m.%d.%Y", ddtype=dateType)
        self.assertEqual(dateType, field4.ddtype)


    def test_should_throw_exception_if_field_created_with_none_datadict_type(self):
        with self.assertRaises(AssertionError):
            TextField(name="Name", code="Q1", label="What is your Name",
                      language="eng", length=TextConstraint(min=4, max=15), ddtype=None)

    def test_should_convert_ddtype_to_json(self):
        expected_json = {
            "defaultValue": "",
            "label": {"eng": "What is your name"},
            "name": "field1_Name",
            "code": "Q1",
            "length": {},
            "type": "text",
            "ddtype": self.DDTYPE_JSON,
            "entity_question_flag": True
        }
        field = TextField(name="field1_Name", code="Q1", label="What is your name",
                             entity_question_flag=True, ddtype=self.ddtype)
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)
        self.assertEqual(self.ddtype, field.ddtype)

    def test_should_return_default_language_text(self):
        expected_json = {
            "choices": [{"text": "Lake", "val": None}, {"text": "Dam", "val": None}],
            "name": "type",
            "ddtype": self.DDTYPE_JSON,
            "type": "select1",
            "code": "T",
            "label": {"eng": "What type?"}}
        field = SelectField(name="type", code="T", label="What type?",
                               options=[{"text": {"fr": "lake", "eng": "Lake"}}, {"text": {"fr": "dam", "eng": "Dam"}}],
                               ddtype=self.ddtype,
                               language="eng",
                               single_select_flag=True)
        actual_json = field._to_json_view()
        self.assertEqual(actual_json, expected_json)

    def test_should_create_location_field_type_for_default_english_language(self):
        expected_json = {
            "label": {"eng": "Where do you stay?"},
            "name": "field1_Loc",
            "code": "Q1",
            "type": "location",
            "ddtype": self.DDTYPE_JSON,
            }
        field = LocationField(name="field1_Loc", code="Q1", label="Where do you stay?", ddtype=self.ddtype,
                                 language="eng")
        actual_json = field._to_json()
        self.assertEqual(actual_json, expected_json)

    def test_should_validate_location(self):
        expect_lat_long=(89.1,100.1)
        field = LocationField(name="field1_Loc", code="Q1", label="Where do you stay?", ddtype=self.ddtype,
                                 language="eng")
        actual_lat_long = field.validate(latitude="89.1", longitude="100.1")
        self.assertEqual(expect_lat_long, actual_lat_long)

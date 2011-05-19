# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datetime import datetime

import unittest
from mock import Mock, patch
from datawinners.project import helper
from datawinners.project.models import Project
from mangrove.datastore.database import get_db_manager, DatabaseManager
from mangrove.datastore.datadict import DataDictType
from mangrove.errors.MangroveException import DataObjectNotFound, FormModelDoesNotExistsException
from mangrove.form_model.field import TextField, IntegerField, SelectField
from mangrove.form_model.form_model import FormModel


class TestHelper(unittest.TestCase):

    def setUp(self):
        self.patcher1 = patch("datawinners.project.helper.create_datadict_type")
        self.patcher2 = patch("datawinners.project.helper.get_datadict_type_by_slug")
        self.create_ddtype_mock = self.patcher1.start()
        self.get_datadict_type_by_slug_mock = self.patcher2.start()
        self.create_ddtype_mock.return_value = Mock(spec=DataDictType)
        self.get_datadict_type_by_slug_mock.side_effect = DataObjectNotFound("","","")
        self.dbm = Mock(spec = DatabaseManager)


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_creates_questions_from_dict(self):
        post = [{"title": "q1", "question_code": "qc1", "description": "desc1", "type": "text", "choices": [],
                 "is_entity_question": True, "min_length": 1, "max_length": 15},
                {"title": "q2", "question_code": "qc2", "description": "desc2", "type": "integer", "choices": [],
                 "is_entity_question": False, "range_min": 0, "range_max": 100},
                {"title": "q3", "question_code": "qc3", "description": "desc3", "type": "select",
                 "choices": [{"value": "c1"}, {"value": "c2"}], "is_entity_question": False},
                {"title": "q4", "question_code": "qc4", "description": "desc4", "type": "select1",
                 "choices": [{"value": "c1"}, {"value": "c2"}], "is_entity_question": False}
        ]
        q1 = helper.create_question(post[0],self.dbm)
        q2 = helper.create_question(post[1],self.dbm)
        q3 = helper.create_question(post[2],self.dbm)
        q4 = helper.create_question(post[3],self.dbm)
        self.assertIsInstance(q1, TextField)
        self.assertIsInstance(q2, IntegerField)
        self.assertIsInstance(q3, SelectField)
        self.assertIsInstance(q4, SelectField)
        self.assertEquals(q1._to_json()["length"], {"min": 1, "max": 15})
        self.assertEquals(q2._to_json()["range"], {"min": 0, "max": 100})
        self.assertEquals(q3._to_json()["type"], "select")
        self.assertEquals(q4._to_json()["type"], "select1")

    def test_should_save_questionnaire_from_post(self):
        post = [{"title": "q1", "question_code": "qc1", "type": "text", "choices": [], "is_entity_question": True,
                 "min_length": 1, "max_length": ""},
                {"title": "q2", "question_code": "qc2", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": 100},
                {"title": "q3", "question_code": "qc3", "type": "select", "choices": [{"value": "c1"}, {"value": "c2"}],
                 "is_entity_question": False}
        ]
        q1 = helper.create_question(post[0],self.dbm)
        form_model = FormModel(get_db_manager(), "test", "test", "test", [q1], "test", "test")
        questionnaire = helper.update_questionnaire_with_questions(form_model, post,self.dbm)
        self.assertEqual(3, len(questionnaire.fields))

    def test_should_create_integer_question_with_no_max_constraint(self):
        post = [{"title": "q2", "question_code": "qc2", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": ""}]
        q1 = helper.create_question(post[0],self.dbm)
        self.assertEqual(q1.constraint.max, None)

    def test_should_return_code_title_tuple_list(self):
        ddtype = Mock(spec=DataDictType)
        question1 = TextField(label="entity_question", question_code="ID", name="What is associated entity",
                              language="eng", entity_question_flag=True, ddtype=ddtype)
        question2 = TextField(label="question1_Name", question_code="Q1", name="What is your name",
                              defaultValue="some default value", language="eng", ddtype=ddtype)
        self.assertEquals([("ID", "What is associated entity"), ("Q1", "What is your name")], helper.get_code_and_title([question1, question2]))

    def test_should_create_text_question_with_no_max_length(self):
        post = [{"title": "q1", "question_code": "qc1", "type": "text", "choices": [], "is_entity_question": True,
                 "min_length": 1, "max_length": ""},
                {"title": "q2", "question_code": "qc2", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": 100},
                {"title": "q3", "question_code": "qc3", "type": "select", "choices": [{"value": "c1"}, {"value": "c2"}],
                 "is_entity_question": False}
        ]
        q1 = helper.create_question(post[0],self.dbm)
        self.assertEqual(q1.constraint.max, None)

    def test_should_create_text_question_with_no_max_lengt_and_min_length(self):
        post = [{"title": "q1", "question_code": "qc1", "type": "text", "choices": [], "is_entity_question": True,
                 },
                {"title": "q2", "question_code": "qc2", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": 100},
                {"title": "q3", "question_code": "qc3", "type": "select", "choices": [{"value": "c1"}, {"value": "c2"}],
                 "is_entity_question": False}
        ]
        q1 = helper.create_question(post[0],self.dbm)
        self.assertEqual(q1.constraint.max, None)
        self.assertEqual(q1.constraint.min, None)

    def test_should_return_tuple_list_of_submissions(self):
        questions = [("Q1", "Question 1"), ("Q2", "Question 2")]
        submissions = [
                        {'values': {'q1': 'ans1', 'q2': 'ans2'}, 'channel': 'sms', 'status': True, 'created': datetime(2011, 1, 1), 'error_message': 'error1'},
                        {'values': {'q2': 'ans22'}, 'channel': 'sms', 'status': False, 'created': datetime(2011, 1, 2), 'error_message': 'error2'}
                      ]
        required_submissions = [(datetime(2011, 1, 1), 'sms', True, 'error1', 'ans1', 'ans2',),
                               (datetime(2011, 1, 2), 'sms', False, 'error2', None, 'ans22',),
                              ]
        self.assertEquals(required_submissions, helper.get_submissions(questions, submissions))

    def test_should_create_text_question_with_implicit_ddtype(self):
        post = {"title": "what is your name", "question_code": "qc1", "description": "desc1", "type": "text", "choices": [],
                 "is_entity_question": True, "min_length": 1, "max_length": 15}

        dbm = Mock(spec=DatabaseManager)

        self.create_ddtype_mock.return_value = DataDictType(dbm, "qc1", "what_is_your_name", "text", "what is your name")

        with patch("datawinners.project.helper.get_datadict_type_by_slug") as get_datadict_type_by_slug_mock:
            get_datadict_type_by_slug_mock.side_effect = DataObjectNotFound("", "", "")
            text_question = helper.create_question(post, dbm)

        self.create_ddtype_mock.assert_called_once_with(dbm=dbm, name="qc1", slug="what_is_your_name",
                                                        primitive_type="text", description="what is your name")
        self.assertEqual('qc1', text_question.ddtype.name)
        self.assertEqual("what is your name", text_question.ddtype.description)
        self.assertEqual("what_is_your_name", text_question.ddtype.slug)
        self.assertEqual("text", text_question.ddtype.primitive_type)

    def test_should_create_integer_question_with_implicit_ddtype(self):
        post = {"title": "What is your age", "question_code": "age", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": 100}

        dbm = Mock(spec=DatabaseManager)

        self.create_ddtype_mock.return_value = DataDictType(dbm, "age", "what_is_your_age", "integer", "what is your age")

        with patch("datawinners.project.helper.get_datadict_type_by_slug") as get_datadict_type_by_slug_mock:
            get_datadict_type_by_slug_mock.side_effect = DataObjectNotFound("", "", "")
            integer_question = helper.create_question(post, dbm)

        self.create_ddtype_mock.assert_called_once_with(dbm=dbm, name="age", slug="what_is_your_age",
                                                        primitive_type="integer", description="What is your age")
        self.assertEqual('age', integer_question.ddtype.name)
        self.assertEqual("what is your age", integer_question.ddtype.description)
        self.assertEqual("what_is_your_age", integer_question.ddtype.slug)
        self.assertEqual("integer", integer_question.ddtype.primitive_type)

    def test_should_create_select_question_with_implicit_ddtype(self):
        CODE = "qc3"
        LABEL = "q3"
        SLUG = "q3"
        TYPE = "select"
        post = {"title": LABEL, "question_code": CODE, "type": TYPE, "choices": [{"value": "c1"}, {"value": "c2"}],
                 "is_entity_question": False}

        dbm = Mock(spec=DatabaseManager)

        expected_data_dict = DataDictType(dbm, CODE, SLUG, TYPE, LABEL)
        self.create_ddtype_mock.return_value = expected_data_dict

        with patch("datawinners.project.helper.get_datadict_type_by_slug") as get_datadict_type_by_slug_mock:
            get_datadict_type_by_slug_mock.side_effect = DataObjectNotFound("", "", "")
            integer_question = helper.create_question(post, dbm)

        self.create_ddtype_mock.assert_called_once_with(dbm=dbm, name=CODE, slug=SLUG,
                                                        primitive_type=TYPE, description=LABEL)
        self.assertEqual(expected_data_dict, integer_question.ddtype)

    def test_should_create_select1_question_with_implicit_ddtype(self):
        CODE = "qc3"
        LABEL = "q3"
        SLUG = "q3"
        TYPE = "select1"
        post = {"title": LABEL, "question_code": CODE, "type": TYPE, "choices": [{"value": "c1"}, {"value": "c2"}],
                 "is_entity_question": False}

        dbm = Mock(spec=DatabaseManager)

        expected_data_dict = DataDictType(dbm, CODE, SLUG, TYPE, LABEL)
        self.create_ddtype_mock.return_value = expected_data_dict

        with patch("datawinners.project.helper.get_datadict_type_by_slug") as get_datadict_type_by_slug_mock:
            get_datadict_type_by_slug_mock.side_effect = DataObjectNotFound("", "", "")
            integer_question = helper.create_question(post, dbm)

        self.create_ddtype_mock.assert_called_once_with(dbm=dbm, name=CODE, slug=SLUG,
                                                        primitive_type=TYPE, description=LABEL)
        self.assertEqual(expected_data_dict, integer_question.ddtype)

    def test_should_create_date_question_with_implicit_ddtype(self):
        CODE = "qc3"
        LABEL = "q3"
        SLUG = "q3"
        TYPE = "date"
        post = {"title": LABEL, "question_code": CODE, "type": TYPE, "date_format": "%m.%Y",
                 "is_entity_question": False}

        dbm = Mock(spec=DatabaseManager)

        expected_data_dict = DataDictType(dbm, CODE, SLUG, TYPE, LABEL)
        self.create_ddtype_mock.return_value = expected_data_dict

        with patch("datawinners.project.helper.get_datadict_type_by_slug") as get_datadict_type_by_slug_mock:
            get_datadict_type_by_slug_mock.side_effect = DataObjectNotFound("", "", "")
            integer_question = helper.create_question(post, dbm)

        self.create_ddtype_mock.assert_called_once_with(dbm=dbm, name=CODE, slug=SLUG,
                                                        primitive_type=TYPE, description=LABEL)
        self.assertEqual(expected_data_dict, integer_question.ddtype)

    def test_should_create_an_entity_question_with_implicit_data_dict_type(self):
        NAME = "eid"
        LABEL = "Entity ID"
        SLUG = "entity_id"
        TYPE = "string"
        post = {"entity_type": "Water Point", "name": "Test Project"}
        dbm = Mock(spec=DatabaseManager)

        patcher = patch("datawinners.project.helper.generate_questionnaire_code")
        mock = patcher.start()
        mock.return_value = '001'

        expected_data_dict = DataDictType(dbm, NAME, SLUG, TYPE, LABEL)
        self.create_ddtype_mock.return_value = expected_data_dict

        with patch("datawinners.project.helper.get_datadict_type_by_slug") as get_datadict_type_by_slug_mock:
            get_datadict_type_by_slug_mock.side_effect = DataObjectNotFound("", "", "")
            form_model = helper.create_questionnaire(post, dbm)

        self.create_ddtype_mock.assert_called_once_with(dbm=dbm, name=NAME, slug=SLUG,
                                                        primitive_type=TYPE, description=LABEL)
        self.assertEqual(expected_data_dict, form_model.fields[0].ddtype)

        self.assertEqual(1, len(form_model.fields))
        self.assertEqual(True, form_model.fields[0].is_entity_field)

        patcher.stop()

    def test_should_generate_unique_questionnaire_code(self):
        patcher = patch("datawinners.project.helper.models")
        models_mock = patcher.start()
        patcher1 = patch("datawinners.project.helper.get_form_model_by_code")
        form_code_mock = patcher1.start()
        dbm = Mock(spec=DatabaseManager)

        form_code_mock.side_effect = FormModelDoesNotExistsException('')
        models_mock.get_all_projects.return_value = []
        self.assertEqual(helper.generate_questionnaire_code(dbm), "001")

        myproject = Mock(spec=Project)
        models_mock.get_all_projects.return_value = [myproject]
        self.assertEqual(helper.generate_questionnaire_code(dbm), "002")

        patcher.stop()
        patcher1.stop()

    def test_should_generate_next_questionnaire_code_if_code_already_exists(self):
        patcher = patch("datawinners.project.helper.models")
        models_mock = patcher.start()

        patcher1 = patch("datawinners.project.helper.get_form_model_by_code")
        form_code_mock = patcher1.start()

        dbm = Mock(spec=DatabaseManager)

        myproject = Mock(spec=Project)
        models_mock.get_all_projects.return_value = [myproject]

        def expected_side_effect(*args,**kwargs):
            code = kwargs.get('code') or args[1]
            if code == "003": raise FormModelDoesNotExistsException('')
            if code == "002": return Mock(spec=FormModel)

        form_code_mock.side_effect = expected_side_effect

        self.assertEqual(helper.generate_questionnaire_code(dbm), "003")

        patcher.stop()
        patcher1.stop()





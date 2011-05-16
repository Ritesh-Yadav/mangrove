# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datetime import datetime

import unittest
from mock import Mock, patch
from datawinners.project import helper
from mangrove.datastore.database import get_db_manager, DatabaseManager, DatabaseManager
from mangrove.datastore.datadict import DataDictType
from mangrove.form_model.field import TextField, IntegerField, SelectField
from mangrove.form_model.form_model import FormModel


class TestHelper(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("datawinners.project.helper.create_ddtype")
        self.create_ddtype_mock = self.patcher.start()
        self.create_ddtype_mock.return_value = Mock(spec=DataDictType)

    def tearDown(self):
        self.patcher.stop()

    def test_creates_questions_from_dict(self):
        post = [{"title": "q1", "code": "qc1", "description": "desc1", "type": "text", "choices": [],
                 "is_entity_question": True, "min_length": 1, "max_length": 15},
                {"title": "q2", "code": "qc2", "description": "desc2", "type": "integer", "choices": [],
                 "is_entity_question": False, "range_min": 0, "range_max": 100},
                {"title": "q3", "code": "qc3", "description": "desc3", "type": "select",
                 "choices": [{"text":"choice1", "value": "c1"}, {"text":"choice2", "value": "c2"}], "is_entity_question": False,
                 "answers_permitted": "single"},
                {"title": "q4", "code": "qc4", "description": "desc4", "type": "select1",
                 "choices": [{"text":"choice1", "value": "c1"}, {"text":"choice2", "value": "c2"}], "is_entity_question": False,
                 "answers_permitted": "single"}
        ]
        q1 = helper.create_question(post[0])
        q2 = helper.create_question(post[1])
        q3 = helper.create_question(post[2])
        q4 = helper.create_question(post[3])
        self.assertIsInstance(q1, TextField)
        self.assertIsInstance(q2, IntegerField)
        self.assertIsInstance(q3, SelectField)
        self.assertIsInstance(q4, SelectField)
        self.assertEquals(q1._to_json()["length"], {"min": 1, "max": 15})
        self.assertEquals(q2._to_json()["range"], {"min": 0, "max": 100})
        self.assertEquals(q3._to_json()["type"], "select")
        self.assertEquals(q4._to_json()["type"], "select1")

    def test_should_save_questionnaire_from_post(self):
        post = [{"title": "q1", "code": "qc1", "type": "text", "choices": [{"text":""}], "is_entity_question": True,
                 "min_length": 1, "max_length": ""},
                {"title": "q2", "code": "qc2", "type": "integer", "choices": [{"text":""}], "is_entity_question": False,
                 "range_min": 0, "range_max": 100},
                {"title": "q3", "code": "qc3", "type": "select", "choices": [{"text":"choice 1", "value": "c1"}, {"text": "choice 2", "value": "c2"}],
                 "is_entity_question": False, "answers_permitted": "single"}
        ]
        q1 = helper.create_question(post[0])
        form_model = FormModel(get_db_manager(), "test", "test", "test", [q1], "test", "test")
        questionnaire = helper.update_questionnaire_with_questions(form_model, post)
        self.assertEqual(3, len(questionnaire.fields))

    def test_should_create_integer_question_with_no_max_constraint(self):
        post = [{"title": "q2", "code": "qc2", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": ""}]
        q1 = helper.create_question(post[0])
        self.assertEqual(q1.constraint.max, None)

    def test_should_return_code_title_tuple_list(self):
        ddtype = Mock(spec = DataDictType)
        question1 = TextField(label="entity_question", question_code="ID", name="What is associated entity",
                              language="eng", entity_question_flag=True, ddtype=ddtype)
        question2 = TextField(label="question1_Name", question_code="Q1", name="What is your name",
                              defaultValue="some default value", language="eng", ddtype=ddtype)
        self.assertEquals([("ID", "What is associated entity"), ("Q1", "What is your name")], helper.get_code_and_title([question1, question2]))

    def test_should_create_text_question_with_no_max_length(self):
        post = [{"title": "q1", "code": "qc1", "type": "text", "choices": [], "is_entity_question": True,
                 "min_length": 1, "max_length": ""},
                {"title": "q2", "code": "qc2", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": 100},
                {"title": "q3", "code": "qc3", "type": "select", "choices": [{"value": "c1"}, {"value": "c2"}],
                 "is_entity_question": False, "answers_permitted": "single"}
        ]
        q1 = helper.create_question(post[0])
        self.assertEqual(q1.constraint.max, None)

    def test_should_create_text_question_with_no_max_lengt_and_min_length(self):
        post = [{"title": "q1", "code": "qc1", "type": "text", "choices": [], "is_entity_question": True,
                 },
                {"title": "q2", "code": "qc2", "type": "integer", "choices": [], "is_entity_question": False,
                 "range_min": 0, "range_max": 100},
                {"title": "q3", "code": "qc3", "type": "select", "choices": [{"value": "c1"}, {"value": "c2"}],
                 "is_entity_question": False, "answers_permitted": "single"}
        ]
        q1 = helper.create_question(post[0])
        self.assertEqual(q1.constraint.max, None)
        self.assertEqual(q1.constraint.min, None)

    def test_should_return_tuple_list_of_submissions(self):
        questions = [("Q1", "Question 1"), ("Q2", "Question 2")]
        submissions = [
                        {'values': {'Q1': 'ans1', 'Q2': 'ans2'}, 'channel': 'sms', 'status': True, 'created': datetime(2011, 1, 1), 'error_message': 'error1'},
                        {'values': {'Q2': 'ans22'}, 'channel': 'sms', 'status': False, 'created': datetime(2011, 1, 2), 'error_message': 'error2'}
                      ]
        required_submissions = [(datetime(2011, 1, 1), 'sms', True, 'error1', 'ans1', 'ans2',),
                               (datetime(2011, 1, 2), 'sms', False, 'error2', None, 'ans22',),
                              ]
        self.assertEquals(required_submissions, helper.get_submissions(questions, submissions))

    def test_should_create_question_with_implicit_ddtype(self):
        post = {"title": "what is your name", "code": "qc1", "description": "desc1", "type": "text", "choices": [],
                 "is_entity_question": True, "min_length": 1, "max_length": 15}

        dbm = Mock(spec=DatabaseManager)

        self.create_ddtype_mock.return_value = DataDictType(dbm,"qc1","what_is_your_name","text","what is your name")
        text_question = helper.create_question(post,dbm)

        self.create_ddtype_mock.assert_called_once_with(dbm = dbm,name = "qc1",slug = "what_is_your_name",
                                                        primitive_type = "text", description = "what is your name")
        self.assertEqual('qc1',text_question.ddtype.name)
        self.assertEqual("what is your name",text_question.ddtype.description)
        self.assertEqual("what_is_your_name",text_question.ddtype.slug)
        self.assertEqual("text",text_question.ddtype.primitive_type)


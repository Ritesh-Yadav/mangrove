# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from unittest.case import TestCase
from mock import Mock, patch
from mangrove.datastore.database import DatabaseManager
from mangrove.datastore.entity import Entity
from mangrove.errors.MangroveException import  NumberNotRegisteredException, SMSParserInvalidFormatException, MultipleSubmissionsForSameCodeException, SubmissionParseException
from mangrove.form_model.form_model import  NAME_FIELD
from mangrove.transport.player.player import SMSPlayer, Request, TransportInfo
from mangrove.transport.submissions import SubmissionHandler


class TestSMSPlayer(TestCase):
    def setUp(self):
        self.dbm = Mock(spec=DatabaseManager)
        self.submission_handler_mock = Mock(spec=SubmissionHandler)
        self.reporter_patcher = patch('mangrove.transport.player.player.reporter')
        self.reporter_module = self.reporter_patcher.start()
        self.reporter_module.find_reporter.return_value = [{NAME_FIELD: "1234"}]
        self.transport = TransportInfo(transport="sms", source="1234", destination="5678")
        self.request = Request( transportInfo=self.transport, message="FORM_CODE +ID 1 +M hello world")
        self.sms_player = SMSPlayer(self.dbm, self.submission_handler_mock)
        self.generate_code_patcher = patch("mangrove.transport.player.player._generate_short_code_if_registration_form")
        self.generate_code_patcher.start()

    def tearDown(self):
        self.reporter_patcher.stop()
        self.generate_code_patcher.stop()

    def test_should_submit_if_parsing_is_successful(self):
        self.sms_player.accept(self.request)

        self.assertEqual(1, self.submission_handler_mock.accept.call_count)

    def test_should_submit_if_submission_by_registered_reporter(self):
        reporter = Mock(spec=Entity)
        self.reporter_module.find_reporter_entity.return_value = reporter

        self.sms_player.accept(self.request)

        self.assertEqual(1, self.submission_handler_mock.accept.call_count)
        submission_request = self.submission_handler_mock.accept.call_args[0][0]
        self.assertEqual(reporter, submission_request.reporter)

    def test_should_check_if_submission_by_unregistered_reporter(self):
        self.reporter_module.find_reporter_entity.side_effect = NumberNotRegisteredException("1234")
        with self.assertRaises(NumberNotRegisteredException):
            self.sms_player.accept(self.request)


    def test_should_not_submit_if_parsing_is_not_successful(self):
        self.request = Request(transportInfo=self.transport, message="invalid format")
        with self.assertRaises(SubmissionParseException):
            self.sms_player.accept(self.request)

        self.assertEqual(0, self.submission_handler_mock.accept.call_count)


    def test_should_not_parse_if_two_question_codes(self):
        transport = TransportInfo(transport="sms", source="1234", destination="5678")
        self.request = Request(transportInfo=transport, message="cli001 +na tester1 +na tester2")
        with self.assertRaises(SubmissionParseException):
            self.sms_player.accept(self.request)

        self.assertEqual(0, self.submission_handler_mock.accept.call_count)



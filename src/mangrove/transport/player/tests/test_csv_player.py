# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import unittest
from mock import Mock, patch
from mangrove.datastore.database import DatabaseManager
from mangrove.errors.MangroveException import FormModelDoesNotExistsException
from mangrove.form_model.form_model import FormModel
from mangrove.transport.player import player
from mangrove.transport.player.parser import CsvParser
from mangrove.transport.player.player import FilePlayer, Channel
from mangrove.transport.submissions import SubmissionLogger


class TestCsvPlayer(unittest.TestCase):
    def _mock_short_code_generator(self):
        self.original_code_generator = player._set_short_code
        self.original_handler_for_reg_form = player.Player._update_submission_with_short_code_if_registration_form
        player._set_short_code = Mock(spec=player._set_short_code)
        player.Player._update_submission_with_short_code_if_registration_form = Mock(
            spec=player.Player._update_submission_with_short_code_if_registration_form)

    def _mock_form_model(self):
        self.get_form_model_mock_patcher = patch('mangrove.transport.player.player.get_form_model_by_code')
        get_form_model_mock = self.get_form_model_mock_patcher.start()
        self.form_model_mock = Mock(spec=FormModel)
        get_form_model_mock.return_value = self.form_model_mock

    def setUp(self):
        self.dbm = Mock(spec=DatabaseManager)
        loc_tree = Mock()
        loc_tree.get_hierarchy_path.return_value = None
        self.parser = CsvParser()

        self.csv_data = """
                                FORM_CODE,ID,BEDS,DIRECTOR,MEDS
                                CLF1,CL001,10,Dr. A,201
                                CLF1,CL002,11,Dr. B,202
                                CLF2,CL003,12,Dr. C,203
                                CLF1,CL004,13,Dr. D,204
                                CLF1,CL005,14,Dr. E,205
"""
        self._mock_short_code_generator()
        self._mock_form_model()
        self.submission_logger = Mock(spec=SubmissionLogger)
        self.player = FilePlayer(self.dbm, self.parser, Channel.CSV, loc_tree, self.submission_logger)

    def tearDown(self):
        player._set_short_code = self.original_code_generator
        player.Player._update_submission_with_short_code_if_registration_form = self.original_handler_for_reg_form
        self.get_form_model_mock_patcher.stop()

    def test_should_import_csv_string(self):
        self.player.accept(self.csv_data)
        self.assertEqual(5, self.form_model_mock.submit.call_count)

    def test_should_process_next_submission_if_exception_with_prev(self):
        def expected_side_effect(*args, **kwargs):
            values = kwargs.get('values') or args[1]
            if values.get('id') == 'CL003':
                raise FormModelDoesNotExistsException('')
            form_submission_mock = Mock()
            form_submission_mock.saved.return_value = True
            form_submission_mock.errors = {}
            return form_submission_mock

        self.form_model_mock.submit.side_effect = expected_side_effect

        response = self.player.accept(self.csv_data)
        self.assertEqual(5, len(response))
        self.assertEqual(False, response[2].success)

        success = len([index for index in response if index.success])
        total = len(response)
        self.assertEqual(4, success)
        self.assertEqual(5, total)

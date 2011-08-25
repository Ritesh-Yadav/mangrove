# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import os
import unittest
from mock import Mock, patch
from mangrove.datastore.database import DatabaseManager
from mangrove.errors.MangroveException import FormModelDoesNotExistsException
from mangrove.form_model.form_model import FormModel
from mangrove.transport.player.parser import XlsParser
from mangrove.transport.player.player import FilePlayer, Channel
import xlwt
from mangrove.transport.submissions import SubmissionLogger

class TestXlsPlayer(unittest.TestCase):
    def _mock_form_model(self):
        self.get_form_model_mock_patcher = patch('mangrove.transport.player.player.get_form_model_by_code')
        get_form_model_mock = self.get_form_model_mock_patcher.start()
        self.form_model_mock = Mock(spec=FormModel)
        get_form_model_mock.return_value = self.form_model_mock

    def setUp(self):
        loc_tree = Mock()
        loc_tree.get_hierarchy_path.return_value = None
        self.dbm = Mock(spec=DatabaseManager)
        self._mock_form_model()
        self.submission_logger = Mock(spec=SubmissionLogger)
        self.parser = XlsParser()
        self.xls_data = """
                                FORM_CODE,ID,BEDS,DIRECTOR,MEDS
                                CLF1,CL001,10,Dr. A,201
                                CLF1,CL002,11,Dr. B,202

                                CLF2,CL003,12,Dr. C,203
                                CLF1,CL004,13,Dr. D,204
                                
                                CLF1,CL005,14,Dr. E,205
"""
        self.file_name = 'test.xls'
        wb = xlwt.Workbook()
        ws = wb.add_sheet('test')
        for row_number, row  in enumerate(self.xls_data.split('\n')):
            for col_number, val in enumerate(row.split(',')):
                ws.write(row_number, col_number, val)
        wb.save(self.file_name)
        self.player = FilePlayer(self.dbm, self.parser, Channel.XLS, loc_tree, self.submission_logger)
        self.generate_code_patcher = patch(
            "mangrove.transport.player.player.Player._update_submission_with_short_code_if_registration_form")
        self.generate_code_patcher.start()

    def tearDown(self):
        self.generate_code_patcher.stop()

    def test_should_import_xls_string(self):
        self.player.accept(file_contents=open(self.file_name).read())
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

        response = self.player.accept(file_contents=open(self.file_name).read())
        self.assertEqual(5, len(response))
        self.assertEqual(False, response[2].success)

        success = len([index for index in response if index.success])
        total = len(response)
        self.assertEqual(4, success)
        self.assertEqual(5, total)

    def tearDown(self):
        os.remove(self.file_name)

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from psycopg2.tests.testutils import unittest
from mangrove.datastore.database import get_db_manager, _delete_db_and_remove_db_manager

class MangroveTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = get_db_manager('http://localhost:5984/', 'mangrove-test')

    def tearDown(self):
        _delete_db_and_remove_db_manager(self.manager)


  
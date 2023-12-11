import unittest
from unittest.mock import patch
from engine import create_connection_string, get_engine

class TestEngine(unittest.TestCase):

    @patch('os.getenv')
    def test_create_connection_string_dw(self, mock_getenv):
        mock_getenv.side_effect = ['dw_address', 'dw_database', None, None]
        expected = 'DRIVER=ODBC Driver 17 for SQL Server;SERVER=dw_address;DATABASE=dw_database;Trusted_Connection=yes;'
        self.assertEqual(create_connection_string('dw'), expected)

    @patch('os.getenv')
    def test_create_connection_string_qnxt(self, mock_getenv):
        mock_getenv.side_effect = ['qnxt_address', 'qnxt_database', 'qnxt_username', 'qnxt_password']
        expected = 'DRIVER=ODBC Driver 17 for SQL Server;SERVER=qnxt_address;DATABASE=qnxt_database;UID=qnxt_username;PWD=qnxt_password;'
        self.assertEqual(create_connection_string('qnxt'), expected)

    @patch('os.getenv')
    def test_create_connection_string_invalid(self, mock_getenv):
        mock_getenv.side_effect = [None, None, None, None]
        with self.assertRaises(ValueError):
            create_connection_string('invalid')

    # Test get_engine
    @patch('engine.create_engine')
    def test_get_engine(self, mock_create_engine):
        mock_create_engine.return_value = 'engine'
        self.assertEqual(get_engine('connection_string'), 'engine')

if __name__ == '__main__':
    unittest.main()

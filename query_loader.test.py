import unittest
from unittest.mock import mock_open, patch
from query_loader import load_queries, load_sql_file

class TestLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"test_query": {"id": "123"}}')
    def test_load_queries(self, mock_file):
        expected = {"test_query": {"id": "123"}}
        self.assertEqual(load_queries('dummy_path'), expected)

    @patch('builtins.open', new_callable=mock_open, read_data='SELECT * FROM table')
    def test_load_sql_file(self, mock_file):
        expected = 'SELECT * FROM table'
        self.assertEqual(load_sql_file('dummy_path'), expected)

    # Add more tests to cover different file contents, file not found scenarios, etc.

if __name__ == '__main__':
    unittest.main()

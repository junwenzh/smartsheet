import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import smartsheet
from update_or_append import update_or_append

class TestUpdateOrAppend(unittest.TestCase):

    @patch('smartsheet.Smartsheet')
    def test_successful_update_or_append(self, mock_smartsheet):
        # Set up mock objects and responses
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_sheet.columns = [MagicMock(id=1, title='Column1'), MagicMock(id=2, title='Column2')]
        mock_sheet.rows = []
        mock_sheet.name = 'Test Sheet'
        mock_client.Sheets.get_sheet.return_value = mock_sheet
        mock_smartsheet.return_value = mock_client

        # Test data
        sheet_id = '123'
        df = pd.DataFrame({'Column1': [1, 2], 'Column2': [3, 4]})
        primary_column_name = 'Column1'

        # Call the function
        result = update_or_append(sheet_id, df, primary_column_name)

        # Assertions
        self.assertTrue(result)
        mock_client.Sheets.get_sheet.assert_called_with(sheet_id)
        mock_client.Sheets.add_rows.assert_called()

    # Test for when the sheet is not found
    @patch('smartsheet.Smartsheet')
    def test_sheet_not_found(self, mock_smartsheet):
        # Set up mock objects and responses
        mock_client = MagicMock()
        mock_client.Sheets.get_sheet.return_value = None
        mock_smartsheet.return_value = mock_client

        # Test data
        sheet_id = '123'
        df = pd.DataFrame({'Column1': [1, 2], 'Column2': [3, 4]})
        primary_column_name = 'Column1'

        # Call the function
        result = update_or_append(sheet_id, df, primary_column_name)

        # Assertions
        self.assertFalse(result)
        mock_client.Sheets.get_sheet.assert_called_with(sheet_id)
        mock_client.Sheets.add_rows.assert_not_called()

    # Test for when not all columns in the DataFrame are in the Smartsheet
    @patch('smartsheet.Smartsheet')
    def test_columns_not_matching(self, mock_smartsheet):
        # Set up mock objects and responses
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_sheet.columns = [MagicMock(id=1, title='Column1'), MagicMock(id=2, title='Column2')]
        mock_sheet.rows = []
        mock_sheet.name = 'Test Sheet'
        mock_client.Sheets.get_sheet.return_value = mock_sheet
        mock_smartsheet.return_value = mock_client

        # Test data
        sheet_id = '123'
        df = pd.DataFrame({'Column1': [1, 2], 'Column3': [3, 4]})
        primary_column_name = 'Column1'

        # Call the function
        result = update_or_append(sheet_id, df, primary_column_name)

        # Assertions
        self.assertFalse(result)
        mock_client.Sheets.get_sheet.assert_called_with(sheet_id)
        mock_client.Sheets.add_rows.assert_not_called()

if __name__ == '__main__':
    unittest.main()

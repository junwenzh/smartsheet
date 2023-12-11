import smartsheet
import pandas as pd
from typing import Any
import logging
import os
from dotenv import load_dotenv

load_dotenv()

def update_or_append(sheet_id: str, df: pd.DataFrame, primary_column_name: str) -> bool:
    """
    Update or append rows to a Smartsheet based on the primary column value.

    Args:
        api_key (str): Smartsheet API key.
        sheet_id (str): ID of the Smartsheet to update/append.
        df (pd.DataFrame): DataFrame containing the data to be updated/appended.
        primary_column_name (str): Name of the primary column in the DataFrame and Smartsheet.

    This function updates rows in a Smartsheet if a matching primary column value is found.
    If no match is found, it appends the row as a new entry. Errors are logged for troubleshooting.
    """
    try:
        api_key = os.getenv('SMARTSHEET_API_KEY')

        # Initialize client
        smartsheet_client = smartsheet.Smartsheet(api_key)

        # Load the entire sheet
        sheet = smartsheet_client.Sheets.get_sheet(sheet_id)

        # Log the sheet ID and name
        # If the sheet is not found, log an error
        if not sheet:
            logging.error(f"Smartsheet ID {sheet_id} not found.")
            return False
        else:
            logging.info(f"Loaded Smartsheet {sheet.name} with ID {sheet_id}")

        # Mapping DataFrame columns to Smartsheet column IDs
        column_map = {col.title: col.id for col in sheet.columns}

        # Get the primary column ID
        primary_column_id = column_map.get(primary_column_name)

        # If not all columns in the DataFrame are in the Smartsheet, log an error
        if not all(col in column_map for col in df.columns):
            logging.error(f"Not all columns in the DataFrame are in the Smartsheet. Please check the column names.")
            return False

        # Prepare rows to update or add
        rows_to_update = []
        rows_to_add = []

        for index, row in df.iterrows():
            # Find the row in the Smartsheet that matches the primary column value
            existing_row = next((r for r in sheet.rows if r.get_column(primary_column_id).value == row[primary_column_name]), None)

            new_smartsheet_row = smartsheet.models.Row()

            # Add the cells to the row
            new_smartsheet_row.cells = [smartsheet.models.Cell({
                'column_id': column_map[col],
                'value': row[col]
            }) for col in df.columns]

            if existing_row:
                new_smartsheet_row.id = existing_row.id
                rows_to_update.append(new_smartsheet_row)
            else:
                new_smartsheet_row.to_top = False
                rows_to_add.append(new_smartsheet_row)

        # Update existing rows
        if rows_to_update:
            smartsheet_client.Sheets.update_rows(sheet_id, rows_to_update)
            logging.info(f"Updated {len(rows_to_update)} rows in Smartsheet ID {sheet_id}")

        # Add new rows
        if rows_to_add:
            smartsheet_client.Sheets.add_rows(sheet_id, rows_to_add)
            logging.info(f"Added {len(rows_to_add)} new rows to Smartsheet ID {sheet_id}")

        return True

    except Exception as e:
        logging.error(f"An unexpected error occurred in update_or_append: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    # do nothing
    pass

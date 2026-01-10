"""
Google Sheets Manager
Handles authentication and basic operations with Google Sheets
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config


class SheetsManager:
    """Manages connections and operations with Google Sheets"""

    def __init__(self):
        """Initialize the Google Sheets connection"""
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """
        Authenticate with Google Sheets API

        This will:
        1. Check if we have saved credentials (token.json)
        2. If not, prompt you to log in via browser
        3. Save the credentials for next time
        """
        # Check if we have saved credentials
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', config.SCOPES)

        # If credentials don't exist or are invalid, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired credentials
                self.creds.refresh(Request())
            else:
                # Get new credentials by logging in
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError(
                        "credentials.json not found. Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', config.SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save credentials for next time
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        # Build the service
        self.service = build('sheets', 'v4', credentials=self.creds)

    def read_sheet(self, sheet_id, range_name):
        """
        Read data from a Google Sheet

        Args:
            sheet_id: The ID of the Google Sheet
            range_name: The range to read (e.g., 'Sheet1!A1:E10')

        Returns:
            List of rows, where each row is a list of cell values
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            return values

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def write_sheet(self, sheet_id, range_name, values):
        """
        Write data to a Google Sheet

        Args:
            sheet_id: The ID of the Google Sheet
            range_name: The range to write to (e.g., 'Sheet1!A1')
            values: List of rows to write, where each row is a list of values

        Returns:
            The number of cells updated
        """
        try:
            body = {
                'values': values
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            return result.get('updatedCells', 0)

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def append_row(self, sheet_id, range_name, values):
        """
        Append a new row to the end of a Google Sheet

        Args:
            sheet_id: The ID of the Google Sheet
            range_name: The range/sheet to append to (e.g., 'Sheet1!A:E')
            values: List of values for the new row

        Returns:
            The range of cells that were updated
        """
        try:
            body = {
                'values': [values]  # Wrap in list to make it a single row
            }
            result = self.service.spreadsheets().values().append(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            return result.get('updates', {}).get('updatedRange', '')

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def find_row_by_value(self, sheet_id, range_name, column_index, search_value):
        """
        Find a row in the sheet that contains a specific value in a specific column

        Args:
            sheet_id: The ID of the Google Sheet
            range_name: The range to search (e.g., 'Sheet1!A:E')
            column_index: The column index to search (0-based, so 0 = column A)
            search_value: The value to search for

        Returns:
            Tuple of (row_number, row_data) if found, or (None, None) if not found
        """
        data = self.read_sheet(sheet_id, range_name)

        if not data:
            return None, None

        for row_num, row in enumerate(data, start=1):
            if len(row) > column_index and row[column_index] == search_value:
                return row_num, row

        return None, None

    def update_cell(self, sheet_id, cell_address, value):
        """
        Update a single cell

        Args:
            sheet_id: The ID of the Google Sheet
            cell_address: The cell to update (e.g., 'Sheet1!A1')
            value: The value to write

        Returns:
            True if successful, False otherwise
        """
        result = self.write_sheet(sheet_id, cell_address, [[value]])
        return result is not None and result > 0

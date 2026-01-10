"""
Configuration file for networking tracker
Loads settings from .env file if present, otherwise uses defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Your Google Sheet IDs (the long string in the URL)
# These can be set in .env file or use the defaults below
FINTECH_SHEET_ID = os.getenv('FINTECH_SHEET_ID', '1Ir2nA37z9iNxVCKHbhSSNK_VJsI49f6N')
HEALTHTECH_SHEET_ID = os.getenv('HEALTHTECH_SHEET_ID', '1Y4djqEJoGqLuxLaMlDpa5DKjkWl3Zhf9')

# The name of the sheet/tab within each spreadsheet
# You may need to update these based on your actual sheet names
FINTECH_SHEET_NAME = os.getenv('FINTECH_SHEET_NAME', 'Sheet1')
HEALTHTECH_SHEET_NAME = os.getenv('HEALTHTECH_SHEET_NAME', 'Sheet1')

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

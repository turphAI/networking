"""
Configuration file for networking tracker
Store your Google Sheet IDs here
"""

# Your Google Sheet IDs (the long string in the URL)
FINTECH_SHEET_ID = "1Ir2nA37z9iNxVCKHbhSSNK_VJsI49f6N"
HEALTHTECH_SHEET_ID = "1Y4djqEJoGqLuxLaMlDpa5DKjkWl3Zhf9"

# The name of the sheet/tab within each spreadsheet
# You may need to update these based on your actual sheet names
FINTECH_SHEET_NAME = "Sheet1"  # Update this to match your actual sheet tab name
HEALTHTECH_SHEET_NAME = "Sheet1"  # Update this to match your actual sheet tab name

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

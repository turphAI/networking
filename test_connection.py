#!/usr/bin/env python3
"""
Test Google Sheets Connection
Verifies credentials and checks sheet structure
"""

import sys
from sheets_manager import SheetsManager
import config

def test_connection():
    """Test connection and print sheet info"""
    print("🔍 Testing Google Sheets connection...\n")

    # Check credentials file
    import os
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        print("\n   Make sure you're running this from the directory containing credentials.json")
        return False

    print("✅ credentials.json found")

    # Try to authenticate
    print("\n🔐 Authenticating with Google...")
    print("   (A browser window should open for authorization)")

    try:
        sheets = SheetsManager()
        print("✅ Authentication successful!\n")
    except Exception as e:
        print(f"❌ Authentication failed: {e}\n")
        return False

    # Try to read sheet metadata
    print("📊 Checking Fintech sheet structure...")
    sheet_id = config.FINTECH_SHEET_ID

    try:
        # Get sheet metadata to see all tabs
        spreadsheet = sheets.service.spreadsheets().get(
            spreadsheetId=sheet_id
        ).execute()

        print(f"✅ Successfully connected to sheet: {spreadsheet['properties']['title']}\n")

        print("📑 Available tabs:")
        for sheet in spreadsheet['sheets']:
            tab_name = sheet['properties']['title']
            print(f"   - {tab_name}")

        print("\n💡 Make sure your config.py uses the exact tab names shown above!")

        return True

    except Exception as e:
        print(f"❌ Failed to read sheet: {e}")
        print(f"\n🔍 Sheet ID being used: {sheet_id}")
        print("   Make sure this is correct!")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

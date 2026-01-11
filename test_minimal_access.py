#!/usr/bin/env python3
"""
Minimal test - try to read just one cell
"""

from sheets_manager import SheetsManager
import config

print("🔍 Testing minimal sheet access...\n")

sheets = SheetsManager()
sheet_id = config.FINTECH_SHEET_ID

print(f"Sheet ID: {sheet_id}")
print(f"Attempting to read cell A1 from 'New England' tab...\n")

try:
    # Try the simplest possible operation - read one cell
    result = sheets.service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range="New England!A1"
    ).execute()

    print("✅ SUCCESS!")
    print(f"Cell A1 contains: {result.get('values', [['']])[0]}")

except Exception as e:
    print(f"❌ FAILED: {e}\n")

    # Try without the tab name
    print("Trying to read Sheet1!A1 instead...")
    try:
        result = sheets.service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range="Sheet1!A1"
        ).execute()
        print("✅ SUCCESS with Sheet1!")
        print(f"Cell A1 contains: {result.get('values', [['']])[0]}")
    except Exception as e2:
        print(f"❌ Also failed: {e2}\n")

        # Try getting spreadsheet metadata
        print("Trying to get spreadsheet metadata...")
        try:
            metadata = sheets.service.spreadsheets().get(
                spreadsheetId=sheet_id,
                fields="properties.title,sheets.properties.title"
            ).execute()
            print("✅ Metadata retrieved!")
            print(f"Title: {metadata['properties']['title']}")
            print("Tabs:")
            for sheet in metadata['sheets']:
                print(f"  - {sheet['properties']['title']}")
        except Exception as e3:
            print(f"❌ Metadata also failed: {e3}")
            print("\n🚨 This sheet ID cannot be accessed at all via the API")
            print("   Possible reasons:")
            print("   1. This might be a Google Workspace sheet with API restrictions")
            print("   2. The sheet might be in a restricted organization")
            print("   3. The file type might not be a standard Google Sheet")

#!/usr/bin/env python3
"""
Test access to the copied fintech sheet
"""

from sheets_manager import SheetsManager

print("🔍 Testing access to copied fintech sheet...\n")

sheets = SheetsManager()

# New copied sheet ID
copied_sheet_id = "1ziKpAHcg6loFZiJ03evsHOpybTVUrSIrEPXKUp8i07k"

print(f"Copied Sheet ID: {copied_sheet_id}\n")

# Try to get metadata
print("1. Getting spreadsheet metadata...")
try:
    metadata = sheets.service.spreadsheets().get(
        spreadsheetId=copied_sheet_id,
        fields="properties.title,sheets.properties.title"
    ).execute()

    print("✅ SUCCESS!")
    print(f"   Title: {metadata['properties']['title']}")
    print("\n   Tabs found:")
    for sheet in metadata['sheets']:
        print(f"     - {sheet['properties']['title']}")

    # Check for the expected tabs
    tab_names = [sheet['properties']['title'] for sheet in metadata['sheets']]
    expected_tabs = ['Dashboard', 'New England', 'NYC', 'Organizations & Events', 'Design Contacts']

    print("\n2. Checking tab structure...")
    for expected in expected_tabs:
        if expected in tab_names:
            print(f"   ✅ Found '{expected}'")
        else:
            print(f"   ⚠️  Missing '{expected}'")

    # Try to read from New England tab
    print("\n3. Testing read from 'New England' tab...")
    result = sheets.service.spreadsheets().values().get(
        spreadsheetId=copied_sheet_id,
        range="New England!A1:M1"
    ).execute()

    print("✅ Can read from New England tab!")
    headers = result.get('values', [[]])[0] if result.get('values') else []
    if headers:
        print(f"   Headers: {headers[:5]}...")

    print("\n🎉 This sheet works with the API!")
    print("\n📝 Next step: Update your .env file with this new Sheet ID:")
    print(f"   FINTECH_SHEET_ID={copied_sheet_id}")

except Exception as e:
    print(f"❌ FAILED: {e}")

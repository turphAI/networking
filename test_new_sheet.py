#!/usr/bin/env python3
"""
Test access to the new test sheet
"""

from sheets_manager import SheetsManager

print("🔍 Testing access to new test sheet...\n")

sheets = SheetsManager()

# New test sheet ID
new_sheet_id = "1DK0oDS0BvzJWJc23zkLJiAQo3oPSrywt5OfPlc9hDhQ"

print(f"Test Sheet ID: {new_sheet_id}\n")

# Try to get metadata
print("1. Getting spreadsheet metadata...")
try:
    metadata = sheets.service.spreadsheets().get(
        spreadsheetId=new_sheet_id,
        fields="properties.title,sheets.properties.title"
    ).execute()

    print("✅ SUCCESS!")
    print(f"   Title: {metadata['properties']['title']}")
    print("   Tabs:")
    for sheet in metadata['sheets']:
        print(f"     - {sheet['properties']['title']}")

    # Try to read a cell
    print("\n2. Reading cell A1...")
    result = sheets.service.spreadsheets().values().get(
        spreadsheetId=new_sheet_id,
        range="Sheet1!A1"
    ).execute()

    print("✅ Can read cells!")

    # Try to write to it
    print("\n3. Writing to cell A1...")
    sheets.service.spreadsheets().values().update(
        spreadsheetId=new_sheet_id,
        range="Sheet1!A1",
        valueInputOption="RAW",
        body={"values": [["API Test - Success!"]]}
    ).execute()

    print("✅ Can write to cells!")
    print("\n🎉 API access works perfectly with this new sheet!")
    print("\n💡 This means:")
    print("   - Your credentials and authentication are working correctly")
    print("   - The old sheet (1Ir2nA37z9iNxVCKHbhSSNK_VJsI49f6N) has a problem")
    print("   - Possible causes:")
    print("     • The sheet was created from a Form or other source")
    print("     • The sheet has some corruption or API restrictions")
    print("     • The Sheet ID is somehow incorrect")
    print("\n📋 Solution: You may need to copy the data from the old sheet to a new one")

except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\n🚨 If the new sheet also fails, there's an API configuration issue")

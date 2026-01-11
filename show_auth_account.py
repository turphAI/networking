#!/usr/bin/env python3
"""
Show which Google account is authenticated
"""

import json
from sheets_manager import SheetsManager

print("🔍 Checking authentication...\n")

sheets = SheetsManager()

# Try to get user info from the token
print("📧 Checking which Google account you're authenticated with...\n")

try:
    # Read the token file to see account info
    with open('token.json', 'r') as f:
        token_data = json.load(f)

    print("Token info:")
    if 'client_id' in token_data:
        print(f"  Client ID: {token_data['client_id'][:50]}...")

    # Try to make a basic API call to verify
    print("\n🔐 Making test API call...")

    # Try to access a simple endpoint to get user info
    from googleapiclient.discovery import build

    # Use Drive API to get user info
    drive_service = build('drive', 'v3', credentials=sheets.creds)
    about = drive_service.about().get(fields="user").execute()

    user_info = about.get('user', {})
    print(f"\n✅ Authenticated as:")
    print(f"   Email: {user_info.get('emailAddress', 'Unknown')}")
    print(f"   Name: {user_info.get('displayName', 'Unknown')}")

    print(f"\n💡 Now check:")
    print(f"   1. Open your Google Sheet in the browser")
    print(f"   2. Look at the top-right corner - what email is shown?")
    print(f"   3. Does it match the email above?")
    print(f"\n   If they DON'T match, you need to:")
    print(f"   - Delete token.json")
    print(f"   - Run the script again")
    print(f"   - Sign in with the account that owns the sheet")

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\nTry deleting token.json and re-authenticating:")
    print(f"  rm token.json")
    print(f"  python test_connection.py")

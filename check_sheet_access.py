#!/usr/bin/env python3
"""
Check Sheet Access
Detailed diagnostics for sheet access issues
"""

import sys
from sheets_manager import SheetsManager
import config

def check_sheet_access():
    """Check if we can access the sheet"""
    print("🔍 Checking sheet access...\n")

    sheets = SheetsManager()
    sheet_id = config.FINTECH_SHEET_ID

    print(f"Sheet ID: {sheet_id}")
    print(f"Authenticated as: {sheets.creds.token[:20]}...\n")

    # Try to get basic sheet info
    print("1. Attempting to get sheet metadata...")
    try:
        # Try the most basic operation
        request = sheets.service.spreadsheets().get(spreadsheetId=sheet_id)
        print(f"   Request URL: {request.uri}")

        spreadsheet = request.execute()

        print("   ✅ SUCCESS! Sheet found:")
        print(f"   Title: {spreadsheet['properties']['title']}")
        print(f"   Tabs: {len(spreadsheet['sheets'])}")
        return True

    except Exception as e:
        print(f"   ❌ FAILED: {e}\n")

        # Check if it's a 404 (not found) vs 400 (bad request)
        error_str = str(e)
        if "404" in error_str:
            print("💡 Error 404 means the sheet doesn't exist or you don't have access")
            print("   - Verify the Sheet ID is correct")
            print("   - Make sure you're signed in with the right Google account")
            print("   - Check that the sheet hasn't been deleted")
        elif "400" in error_str:
            print("💡 Error 400 might mean:")
            print("   - The ID points to a non-spreadsheet document (Doc, Form, etc.)")
            print("   - The sheet has been moved to trash")
            print("   - There's an API configuration issue")

        print(f"\n🔧 Try these steps:")
        print(f"   1. Open this URL in your browser:")
        print(f"      https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
        print(f"   2. If it doesn't open, the Sheet ID is wrong")
        print(f"   3. If it asks you to sign in, use the SAME Google account")
        print(f"      that you authenticated with (check token.json)")

        return False

if __name__ == "__main__":
    success = check_sheet_access()
    sys.exit(0 if success else 1)

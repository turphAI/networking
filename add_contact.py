#!/usr/bin/env python3
"""
Add Contact Script
Add a design contact to your Contacts tab for networking

Usage:
    python add_contact.py "Jane Doe" --company "Stripe" --tracker fintech --role "Senior UX Designer"
    python add_contact.py "John Smith" --company "Oscar Health" --tracker healthtech --role "Design Lead" --linkedin "linkedin.com/in/johnsmith"
"""

import argparse
import sys
from datetime import datetime
from sheets_manager import SheetsManager
import config


def add_contact(name, company, tracker_type, role='', linkedin='', background='', notes=''):
    """
    Add a contact to the Contacts tab

    Args:
        name: Contact's name
        company: Company they work at
        tracker_type: Either 'fintech' or 'healthtech'
        role: Their job title/role
        linkedin: LinkedIn profile URL
        background: Background notes about them
        notes: Additional notes
    """
    print(f"\n📋 Adding {name} from {company} to {tracker_type} tracker...")

    # Initialize manager
    sheets = SheetsManager()

    # Get the appropriate sheet ID
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return False

    sheet_name = config.CONTACTS_TAB

    # Check if contact already exists
    print("🔍 Checking if contact already exists...")
    range_name = f"{sheet_name}!A:Z"
    existing_data = sheets.read_sheet(sheet_id, range_name)

    if existing_data:
        for row in existing_data[1:]:  # Skip header row
            if len(row) > 1:
                # Check if same name and company combination exists
                existing_name = row[1] if len(row) > 1 else ''
                existing_company = row[0] if len(row) > 0 else ''
                if (existing_name.lower() == name.lower() and
                    existing_company.lower() == company.lower()):
                    print(f"⚠️  {name} from {company} already exists in Contacts!")
                    return False

    # Prepare row data matching your column structure
    # Columns: Company | Name | Role/Title | LinkedIn Profile | Background Notes |
    #          Contact Status | Last Outreach | Notes
    new_row = [
        company,                                # A: Company
        name,                                   # B: Name
        role,                                   # C: Role/Title
        linkedin,                               # D: LinkedIn Profile
        background,                             # E: Background Notes
        'Not Contacted',                        # F: Contact Status
        '',                                     # G: Last Outreach
        notes                                   # H: Notes
    ]

    # Add to sheet
    print("📝 Adding to Google Sheet...")
    result = sheets.append_row(sheet_id, f"{sheet_name}!A:H", new_row)

    if result:
        print(f"✅ Successfully added {name} to Contacts!")
        print(f"\n📊 Next steps:")
        print(f"   1. Open your sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print(f"   2. Review the contact information")
        print(f"   3. Use update_contact.py to track outreach")

        if linkedin:
            print(f"\n🔗 LinkedIn Profile:")
            print(f"   {linkedin}")

        return True
    else:
        print("❌ Failed to add contact")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Add a new contact to your Contacts tab',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a basic contact
  python add_contact.py "Jane Doe" --company "Stripe" --tracker fintech --role "Senior UX Designer"

  # Add with LinkedIn profile
  python add_contact.py "John Smith" --company "Oscar Health" --tracker healthtech \\
    --role "Design Lead" \\
    --linkedin "https://linkedin.com/in/johnsmith"

  # Add with background notes
  python add_contact.py "Sarah Lee" --company "Plaid" --tracker fintech \\
    --role "Principal Designer" \\
    --background "Met at UX conference, worked at Google before" \\
    --notes "Very interested in fintech UX patterns"
        """
    )
    parser.add_argument(
        'name',
        help='Contact name (e.g., "Jane Doe")'
    )
    parser.add_argument(
        '--company',
        required=True,
        help='Company name'
    )
    parser.add_argument(
        '--tracker',
        choices=['fintech', 'healthtech'],
        required=True,
        help='Which tracker to add the contact to'
    )
    parser.add_argument(
        '--role',
        default='',
        help='Job title/role (e.g., "Senior UX Designer")'
    )
    parser.add_argument(
        '--linkedin',
        default='',
        help='LinkedIn profile URL'
    )
    parser.add_argument(
        '--background',
        default='',
        help='Background notes about the contact'
    )
    parser.add_argument(
        '--notes',
        default='',
        help='Additional notes'
    )

    args = parser.parse_args()

    try:
        add_contact(
            args.name,
            args.company,
            args.tracker,
            args.role,
            args.linkedin,
            args.background,
            args.notes
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

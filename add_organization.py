#!/usr/bin/env python3
"""
Add Organization Script
Add organizations/events to your Organization tab for networking opportunities

Usage:
    python add_organization.py "UXPA Boston" --tracker fintech --location "Boston, MA" --type "Professional Organization"
    python add_organization.py "Health 2.0" --tracker healthtech --location "Virtual" --type "Conference" --timing "Annual"
"""

import argparse
import sys
from sheets_manager import SheetsManager
import config


def add_organization(org_name, tracker_type, location='', org_type='', description='',
                     timing='', contact_website='', notes=''):
    """
    Add an organization or event to the Organization tab

    Args:
        org_name: Name of the organization or event
        tracker_type: Either 'fintech' or 'healthtech'
        location: Location of the org/event
        org_type: Type (e.g., Professional Organization, Conference, Meetup, etc.)
        description: Description of the organization/event
        timing: Timing/frequency (e.g., Annual, Monthly, Quarterly)
        contact_website: Contact info or website
        notes: Additional notes
    """
    print(f"\n📋 Adding {org_name} to {tracker_type} tracker...")

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

    sheet_name = config.ORGANIZATION_TAB

    # Check if organization already exists
    print("🔍 Checking if organization already exists...")
    range_name = f"{sheet_name}!A:Z"
    existing_data = sheets.read_sheet(sheet_id, range_name)

    if existing_data:
        for row in existing_data[1:]:  # Skip header row
            if row and len(row) > 0 and row[0].lower() == org_name.lower():
                print(f"⚠️  {org_name} already exists in Organization tab!")
                return False

    # Prepare row data matching your column structure
    # Columns: Organization/Event | Location | Type | Description |
    #          Timing/Frequency | Contact/Website | Notes
    new_row = [
        org_name,               # A: Organization/Event
        location,               # B: Location
        org_type,               # C: Type
        description,            # D: Description
        timing,                 # E: Timing/Frequency
        contact_website,        # F: Contact/Website
        notes                   # G: Notes
    ]

    # Add to sheet
    print("📝 Adding to Google Sheet...")
    result = sheets.append_row(sheet_id, f"{sheet_name}!A:G", new_row)

    if result:
        print(f"✅ Successfully added {org_name} to Organization tab!")
        print(f"\n📊 Next steps:")
        print(f"   1. Open your sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print(f"   2. Review the organization details")
        print(f"   3. Add any networking events or contacts from this organization")

        if contact_website:
            print(f"\n🔗 Organization website:")
            print(f"   {contact_website}")

        return True
    else:
        print("❌ Failed to add organization")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Add an organization or event to your networking tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a professional organization
  python add_organization.py "UXPA Boston" --tracker fintech \\
    --location "Boston, MA" \\
    --type "Professional Organization" \\
    --description "User Experience Professionals Association" \\
    --contact "https://uxpaboston.org"

  # Add a conference
  python add_organization.py "Health 2.0" --tracker healthtech \\
    --location "Virtual" \\
    --type "Conference" \\
    --timing "Annual - Fall" \\
    --description "Healthcare innovation conference" \\
    --contact "https://health2con.com"

  # Add a meetup group
  python add_organization.py "NYC FinTech Meetup" --tracker fintech \\
    --location "New York, NY" \\
    --type "Meetup" \\
    --timing "Monthly" \\
    --notes "Great for networking with fintech designers"

Organization Types:
  - Professional Organization
  - Conference
  - Meetup
  - Workshop
  - Networking Event
  - Online Community
        """
    )
    parser.add_argument(
        'org_name',
        help='Name of the organization or event'
    )
    parser.add_argument(
        '--tracker',
        choices=['fintech', 'healthtech'],
        required=True,
        help='Which tracker to add the organization to'
    )
    parser.add_argument(
        '--location',
        default='',
        help='Location (city, state, or "Virtual")'
    )
    parser.add_argument(
        '--type',
        default='',
        help='Type of organization (Professional Organization, Conference, Meetup, etc.)'
    )
    parser.add_argument(
        '--description',
        default='',
        help='Description of the organization/event'
    )
    parser.add_argument(
        '--timing',
        default='',
        help='Timing/frequency (Annual, Monthly, Quarterly, etc.)'
    )
    parser.add_argument(
        '--contact',
        default='',
        help='Contact info or website URL'
    )
    parser.add_argument(
        '--notes',
        default='',
        help='Additional notes'
    )

    args = parser.parse_args()

    try:
        add_organization(
            args.org_name,
            args.tracker,
            args.location,
            args.type,
            args.description,
            args.timing,
            args.contact,
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

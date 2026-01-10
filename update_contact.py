#!/usr/bin/env python3
"""
Update Contact Script
Update contact information and status in the Contacts tab

Usage:
    # Update status
    python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech --status "Reached Out"

    # Update notes
    python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech --notes "Met at conference"

    # Update multiple fields
    python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech \\
      --status "Meeting Scheduled" --notes "Coffee chat next week"

    # View current info
    python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech --show
"""

import argparse
import sys
from datetime import datetime
from sheets_manager import SheetsManager
import config


def update_contact_info(name, company, tracker_type, **updates):
    """
    Update information for a contact in the Contacts tab

    Args:
        name: Contact name
        company: Company name
        tracker_type: Either 'fintech' or 'healthtech'
        **updates: Keyword arguments for fields to update
    """
    print(f"\n📝 Updating {name} from {company} in {tracker_type} tracker...")

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

    # Find the contact in the sheet
    # We need to search for both name AND company since names might not be unique
    range_name = f"{sheet_name}!A:Z"
    data = sheets.read_sheet(sheet_id, range_name)

    row_number = None
    row_data = None

    if data:
        for i, row in enumerate(data, start=1):
            if i == 1:  # Skip header
                continue
            if len(row) > 1:
                existing_company = row[0] if len(row) > 0 else ''
                existing_name = row[1] if len(row) > 1 else ''
                if (existing_name.lower() == name.lower() and
                    existing_company.lower() == company.lower()):
                    row_number = i
                    row_data = row
                    break

    if not row_number:
        print(f"❌ Contact '{name}' from '{company}' not found in Contacts tab")
        print("   Use add_contact.py to add them first")
        return False

    print(f"✅ Found {name} in row {row_number}")

    # Update each field
    # Columns: Company (A) | Name (B) | Role/Title (C) | LinkedIn Profile (D) |
    #          Background Notes (E) | Contact Status (F) | Last Outreach (G) | Notes (H)
    updates_made = []

    if 'role' in updates and updates['role'] is not None:
        cell_address = f"{sheet_name}!C{row_number}"
        if sheets.update_cell(sheet_id, cell_address, updates['role']):
            print(f"  ✓ Updated role: {updates['role']}")
            updates_made.append('role')

    if 'linkedin' in updates and updates['linkedin'] is not None:
        cell_address = f"{sheet_name}!D{row_number}"
        if sheets.update_cell(sheet_id, cell_address, updates['linkedin']):
            print(f"  ✓ Updated LinkedIn: {updates['linkedin']}")
            updates_made.append('linkedin')

    if 'background' in updates and updates['background'] is not None:
        cell_address = f"{sheet_name}!E{row_number}"
        if sheets.update_cell(sheet_id, cell_address, updates['background']):
            print(f"  ✓ Updated background: {updates['background']}")
            updates_made.append('background')

    if 'status' in updates and updates['status'] is not None:
        cell_address = f"{sheet_name}!F{row_number}"
        if sheets.update_cell(sheet_id, cell_address, updates['status']):
            print(f"  ✓ Updated status: {updates['status']}")
            updates_made.append('status')

            # If status is being updated to "Reached Out" or similar, update Last Outreach date
            if updates['status'].lower() in ['reached out', 'contacted', 'emailed']:
                today = datetime.now().strftime('%Y-%m-%d')
                cell_address = f"{sheet_name}!G{row_number}"
                if sheets.update_cell(sheet_id, cell_address, today):
                    print(f"  ✓ Updated last outreach: {today}")
                    updates_made.append('last_outreach')

    if 'last_outreach' in updates and updates['last_outreach'] is not None:
        cell_address = f"{sheet_name}!G{row_number}"
        if sheets.update_cell(sheet_id, cell_address, updates['last_outreach']):
            print(f"  ✓ Updated last outreach: {updates['last_outreach']}")
            updates_made.append('last_outreach')

    if 'notes' in updates and updates['notes'] is not None:
        cell_address = f"{sheet_name}!H{row_number}"
        # If there are existing notes, append instead of replace
        existing_notes = row_data[7] if len(row_data) > 7 else ''
        if existing_notes and 'append' in updates and updates['append']:
            new_notes = f"{existing_notes}; {updates['notes']}"
        else:
            new_notes = updates['notes']

        if sheets.update_cell(sheet_id, cell_address, new_notes):
            print(f"  ✓ Updated notes: {new_notes}")
            updates_made.append('notes')

    if updates_made:
        print(f"\n✅ Successfully updated {len(updates_made)} field(s)")
        print(f"   View in sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        return True
    else:
        print("\n⚠️  No updates were made")
        return False


def show_contact_info(name, company, tracker_type):
    """
    Display current information for a contact

    Args:
        name: Contact name
        company: Company name
        tracker_type: Either 'fintech' or 'healthtech'
    """
    print(f"\n📋 Current info for {name} from {company}...")

    sheets = SheetsManager()

    # Get the appropriate sheet ID
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return

    sheet_name = config.CONTACTS_TAB

    # Find the contact
    range_name = f"{sheet_name}!A:Z"
    data = sheets.read_sheet(sheet_id, range_name)

    row_data = None
    if data:
        for i, row in enumerate(data, start=1):
            if i == 1:  # Skip header
                continue
            if len(row) > 1:
                existing_company = row[0] if len(row) > 0 else ''
                existing_name = row[1] if len(row) > 1 else ''
                if (existing_name.lower() == name.lower() and
                    existing_company.lower() == company.lower()):
                    row_data = row
                    break

    if not row_data:
        print(f"❌ Contact '{name}' from '{company}' not found")
        return

    # Display info
    fields = [
        'Company',
        'Name',
        'Role/Title',
        'LinkedIn Profile',
        'Background Notes',
        'Contact Status',
        'Last Outreach',
        'Notes'
    ]

    print("\n" + "=" * 60)
    for i, field in enumerate(fields):
        value = row_data[i] if i < len(row_data) else ''
        print(f"{field:20}: {value}")
    print("=" * 60)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Update contact information and status',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update status
  python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech --status "Reached Out"

  # Update with notes
  python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech \\
    --status "Meeting Scheduled" --notes "Coffee chat on Friday"

  # Append to existing notes
  python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech \\
    --notes "Follow up next month" --append

  # View current info
  python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech --show

Available Status Options:
  - Not Contacted
  - Reached Out
  - Responded
  - Meeting Scheduled
  - Follow Up
  - Not Interested
        """
    )

    parser.add_argument(
        'name',
        help='Contact name'
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
        help='Which tracker to use'
    )
    parser.add_argument(
        '--role',
        help='Update job title/role'
    )
    parser.add_argument(
        '--linkedin',
        help='Update LinkedIn profile URL'
    )
    parser.add_argument(
        '--background',
        help='Update background notes'
    )
    parser.add_argument(
        '--status',
        choices=['Not Contacted', 'Reached Out', 'Responded', 'Meeting Scheduled', 'Follow Up', 'Not Interested'],
        help='Update contact status'
    )
    parser.add_argument(
        '--last-outreach',
        help='Update last outreach date (YYYY-MM-DD format)'
    )
    parser.add_argument(
        '--notes',
        help='Update notes'
    )
    parser.add_argument(
        '--append',
        action='store_true',
        help='Append to existing notes instead of replacing'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Just show current information without updating'
    )

    args = parser.parse_args()

    try:
        if args.show:
            show_contact_info(args.name, args.company, args.tracker)
        else:
            # Collect updates
            updates = {
                'role': args.role,
                'linkedin': args.linkedin,
                'background': args.background,
                'status': args.status,
                'last_outreach': getattr(args, 'last_outreach', None),
                'notes': args.notes,
                'append': args.append
            }

            # Remove None values
            updates = {k: v for k, v in updates.items() if v is not None or k == 'append'}

            if not any(v is not None for k, v in updates.items() if k != 'append'):
                print("\n⚠️  No updates specified. Use --help to see options")
                print("    Or use --show to view current information")
                sys.exit(1)

            update_contact_info(args.name, args.company, args.tracker, **updates)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

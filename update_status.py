#!/usr/bin/env python3
"""
Update Status Script
Update contact information and outreach status for companies in your tracker

Usage:
    # Update contact info
    python update_status.py "Company Name" --tracker fintech --contact "Jane Doe" --title "Senior UX Designer" --email "jane@company.com"

    # Update status only
    python update_status.py "Company Name" --tracker healthtech --status "Reached Out"

    # Update notes
    python update_status.py "Company Name" --tracker fintech --notes "Met at conference, follow up next week"
"""

import argparse
import sys
from sheets_manager import SheetsManager
import config
from datetime import datetime


def update_company_info(company_name, tracker_type, **updates):
    """
    Update information for a company in the tracker

    Args:
        company_name: Name of the company
        tracker_type: Either 'fintech' or 'healthtech'
        **updates: Keyword arguments for fields to update
    """
    print(f"\n📝 Updating {company_name} in {tracker_type} tracker...")

    # Initialize manager
    sheets = SheetsManager()

    # Get the appropriate sheet ID
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
        sheet_name = config.FINTECH_SHEET_NAME
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
        sheet_name = config.HEALTHTECH_SHEET_NAME
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return False

    # Find the company in the sheet
    range_name = f"{sheet_name}!A:Z"
    row_number, row_data = sheets.find_row_by_value(
        sheet_id, range_name, 0, company_name
    )

    if not row_number:
        print(f"❌ Company '{company_name}' not found in {tracker_type} tracker")
        print("   Use add_company.py to add it first")
        return False

    print(f"✅ Found {company_name} in row {row_number}")

    # Column mapping (adjust based on your sheet structure)
    column_map = {
        'website': 'B',
        'linkedin': 'C',
        'contact': 'D',
        'title': 'E',
        'email': 'F',
        'status': 'G',
        'notes': 'H'
    }

    # Update each field
    updates_made = []
    for field, value in updates.items():
        if value is not None and field in column_map:
            column = column_map[field]
            cell_address = f"{sheet_name}!{column}{row_number}"

            success = sheets.update_cell(sheet_id, cell_address, value)

            if success:
                print(f"  ✓ Updated {field}: {value}")
                updates_made.append(field)
            else:
                print(f"  ✗ Failed to update {field}")

    if updates_made:
        print(f"\n✅ Successfully updated {len(updates_made)} field(s)")
        print(f"   View in sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        return True
    else:
        print("\n⚠️  No updates were made")
        return False


def show_company_info(company_name, tracker_type):
    """
    Display current information for a company

    Args:
        company_name: Name of the company
        tracker_type: Either 'fintech' or 'healthtech'
    """
    print(f"\n📋 Current info for {company_name}...")

    sheets = SheetsManager()

    # Get the appropriate sheet ID
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
        sheet_name = config.FINTECH_SHEET_NAME
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
        sheet_name = config.HEALTHTECH_SHEET_NAME
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return

    # Find the company
    range_name = f"{sheet_name}!A:Z"
    row_number, row_data = sheets.find_row_by_value(
        sheet_id, range_name, 0, company_name
    )

    if not row_number:
        print(f"❌ Company '{company_name}' not found")
        return

    # Display info
    fields = [
        'Company Name',
        'Website',
        'LinkedIn',
        'Contact Name',
        'Contact Title',
        'Contact Email',
        'Status',
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
  # Add contact information
  python update_status.py "Stripe" --tracker fintech --contact "Jane Doe" --title "UX Designer"

  # Update outreach status
  python update_status.py "Stripe" --tracker fintech --status "Reached Out"

  # Add notes
  python update_status.py "Stripe" --tracker fintech --notes "Connected on LinkedIn"

  # View current info
  python update_status.py "Stripe" --tracker fintech --show
        """
    )

    parser.add_argument(
        'company_name',
        help='Name of the company'
    )
    parser.add_argument(
        '--tracker',
        choices=['fintech', 'healthtech'],
        required=True,
        help='Which tracker to use'
    )
    parser.add_argument(
        '--website',
        help='Company website URL'
    )
    parser.add_argument(
        '--linkedin',
        help='LinkedIn company page URL'
    )
    parser.add_argument(
        '--contact',
        help='Contact person name'
    )
    parser.add_argument(
        '--title',
        help='Contact person job title'
    )
    parser.add_argument(
        '--email',
        help='Contact person email'
    )
    parser.add_argument(
        '--status',
        choices=['To Research', 'Researched', 'Reached Out', 'Responded', 'Meeting Scheduled', 'Follow Up', 'Not Interested'],
        help='Outreach status'
    )
    parser.add_argument(
        '--notes',
        help='Additional notes'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Just show current information without updating'
    )

    args = parser.parse_args()

    try:
        if args.show:
            show_company_info(args.company_name, args.tracker)
        else:
            # Collect updates
            updates = {
                'website': args.website,
                'linkedin': args.linkedin,
                'contact': args.contact,
                'title': args.title,
                'email': args.email,
                'status': args.status,
                'notes': args.notes
            }

            # Remove None values
            updates = {k: v for k, v in updates.items() if v is not None}

            if not updates:
                print("\n⚠️  No updates specified. Use --help to see options")
                print("    Or use --show to view current information")
                sys.exit(1)

            update_company_info(args.company_name, args.tracker, **updates)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

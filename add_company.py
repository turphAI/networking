#!/usr/bin/env python3
"""
Add Company Script
Add a new company to your networking tracker

Usage:
    python add_company.py "Company Name" --tracker fintech
    python add_company.py "Company Name" --tracker healthtech
"""

import argparse
import sys
from sheets_manager import SheetsManager
from company_researcher import CompanyResearcher
import config


def add_company(company_name, tracker_type):
    """
    Add a company to the specified tracker

    Args:
        company_name: Name of the company to add
        tracker_type: Either 'fintech' or 'healthtech'
    """
    print(f"\n📋 Adding {company_name} to {tracker_type} tracker...")

    # Initialize managers
    sheets = SheetsManager()
    researcher = CompanyResearcher()

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

    # Check if company already exists
    print("🔍 Checking if company already exists...")
    range_name = f"{sheet_name}!A:Z"
    existing_data = sheets.read_sheet(sheet_id, range_name)

    if existing_data:
        for row in existing_data[1:]:  # Skip header row
            if row and row[0].lower() == company_name.lower():
                print(f"⚠️  {company_name} already exists in the tracker!")
                return False

    # Create research template
    print("🔬 Creating research template...")
    research = researcher.create_company_research_template(company_name)

    # Prepare row data
    # Adjust these columns based on your actual sheet structure
    new_row = [
        research['company_name'],      # Column A: Company Name
        research['website'],            # Column B: Website
        research['linkedin_company'],   # Column C: LinkedIn
        '',                             # Column D: Contact Name
        '',                             # Column E: Contact Title
        '',                             # Column F: Contact Email
        research['status'],             # Column G: Status
        research['notes']               # Column H: Notes
    ]

    # Add to sheet
    print("📝 Adding to Google Sheet...")
    result = sheets.append_row(sheet_id, f"{sheet_name}!A:H", new_row)

    if result:
        print(f"✅ Successfully added {company_name}!")
        print(f"\n📊 Next steps:")
        print(f"   1. Open your sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print(f"   2. Fill in the website and LinkedIn company page")
        print(f"   3. Use find_contacts.py to research design contacts")
        print(f"\n🔗 LinkedIn search URL:")
        print(f"   {research['linkedin_search']}")
        return True
    else:
        print("❌ Failed to add company")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Add a new company to your networking tracker'
    )
    parser.add_argument(
        'company_name',
        help='Name of the company to add'
    )
    parser.add_argument(
        '--tracker',
        choices=['fintech', 'healthtech'],
        required=True,
        help='Which tracker to add the company to'
    )

    args = parser.parse_args()

    try:
        add_company(args.company_name, args.tracker)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

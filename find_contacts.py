#!/usr/bin/env python3
"""
Find Contacts Script
Research and find design team contacts for companies in your tracker

Usage:
    python find_contacts.py "Company Name" --tracker fintech
    python find_contacts.py --all --tracker healthtech
"""

import argparse
import sys
from sheets_manager import SheetsManager
from company_researcher import CompanyResearcher
import config


def find_contacts_for_company(company_name, tracker_type):
    """
    Find design contacts for a specific company

    Args:
        company_name: Name of the company
        tracker_type: Either 'fintech' or 'healthtech'
    """
    print(f"\n🔍 Finding contacts for {company_name}...")

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
        return

    # Find the company in the sheet
    range_name = f"{sheet_name}!A:Z"
    row_number, row_data = sheets.find_row_by_value(
        sheet_id, range_name, 0, company_name
    )

    if not row_number:
        print(f"❌ Company '{company_name}' not found in {tracker_type} tracker")
        print("   Use add_company.py to add it first")
        return

    print(f"✅ Found {company_name} in row {row_number}")

    # Get LinkedIn search info
    linkedin_info = researcher.extract_contacts_from_linkedin(company_name)

    print(f"\n📱 Manual Research Required:")
    print("=" * 60)
    print(f"\nBecause of LinkedIn's terms of service, you'll need to manually")
    print(f"search for contacts. Here's how:\n")

    for step in linkedin_info['instructions']:
        print(f"  {step}")

    print(f"\n🔗 Quick Links:")
    if len(row_data) > 1 and row_data[1]:  # Website
        print(f"   Company Website: {row_data[1]}")
    if len(row_data) > 2 and row_data[2]:  # LinkedIn
        print(f"   LinkedIn Company: {row_data[2]}")
    print(f"   LinkedIn Search: {linkedin_info['search_url']}")

    # Check for team pages
    if len(row_data) > 1 and row_data[1]:
        website = row_data[1]
        team_pages = researcher.find_design_team_page(website)
        if team_pages:
            print(f"\n🌐 Potential team pages to check:")
            for page in team_pages[:5]:  # Show first 5
                print(f"   {page}")

    print(f"\n💡 Tips:")
    print(f"   - Look for: UX Designer, Product Designer, Design Lead, Head of Design")
    print(f"   - Check their About page and Team page")
    print(f"   - Once you find contacts, use update_status.py to add them")


def find_all_contacts(tracker_type):
    """
    Find contacts for all companies needing research

    Args:
        tracker_type: Either 'fintech' or 'healthtech'
    """
    print(f"\n🔍 Finding contacts for all companies in {tracker_type} tracker...")

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

    # Read all companies
    range_name = f"{sheet_name}!A:Z"
    data = sheets.read_sheet(sheet_id, range_name)

    if not data or len(data) < 2:
        print("No companies found in tracker")
        return

    # Find companies that need research
    companies_to_research = []
    for i, row in enumerate(data[1:], start=2):  # Skip header
        if row:
            company_name = row[0] if len(row) > 0 else ''
            status = row[6] if len(row) > 6 else ''

            # Look for companies that need research
            if company_name and status.lower() in ['to research', 'needs_research', '']:
                companies_to_research.append(company_name)

    if not companies_to_research:
        print("✅ All companies have been researched!")
        return

    print(f"\n📋 Found {len(companies_to_research)} companies needing research:\n")

    for i, company in enumerate(companies_to_research, 1):
        print(f"{i}. {company}")

    print(f"\n💡 To research each company, run:")
    for company in companies_to_research:
        print(f'   python find_contacts.py "{company}" --tracker {tracker_type}')


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Find design team contacts for companies'
    )
    parser.add_argument(
        'company_name',
        nargs='?',
        help='Name of the company (optional if using --all)'
    )
    parser.add_argument(
        '--tracker',
        choices=['fintech', 'healthtech'],
        required=True,
        help='Which tracker to use'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Show all companies that need research'
    )

    args = parser.parse_args()

    try:
        if args.all:
            find_all_contacts(args.tracker)
        elif args.company_name:
            find_contacts_for_company(args.company_name, args.tracker)
        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

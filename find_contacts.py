#!/usr/bin/env python3
"""
Find Contacts Script
Research and find design team contacts for companies in your tracker

Usage:
    python find_contacts.py "Company Name" --tracker fintech --region new-england
    python find_contacts.py --all --tracker healthtech --region nyc
"""

import argparse
import sys
from sheets_manager import SheetsManager
from company_researcher import CompanyResearcher
import config


def find_contacts_for_company(company_name, tracker_type, region):
    """
    Find design contacts for a specific company

    Args:
        company_name: Name of the company
        tracker_type: Either 'fintech' or 'healthtech'
        region: Either 'new-england' or 'nyc'
    """
    print(f"\n🔍 Finding contacts for {company_name}...")

    # Initialize managers
    sheets = SheetsManager()
    researcher = CompanyResearcher()

    # Get the appropriate sheet ID and tab
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return

    if region.lower() == 'new-england':
        sheet_name = config.NEW_ENGLAND_TAB
    elif region.lower() == 'nyc':
        sheet_name = config.NYC_TAB
    else:
        print("❌ Error: region must be 'new-england' or 'nyc'")
        return

    # Find the company in the sheet
    range_name = f"{sheet_name}!A:Z"
    row_number, row_data = sheets.find_row_by_value(
        sheet_id, range_name, 0, company_name
    )

    if not row_number:
        print(f"❌ Company '{company_name}' not found in {sheet_name}")
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
    # Column E is Website/LinkedIn
    if len(row_data) > 4 and row_data[4]:
        print(f"   Company Website/LinkedIn: {row_data[4]}")
    print(f"   LinkedIn Search: {linkedin_info['search_url']}")

    # Check for team pages if website exists
    if len(row_data) > 4 and row_data[4]:
        website = row_data[4]
        if website.startswith('http'):
            team_pages = researcher.find_design_team_page(website)
            if team_pages:
                print(f"\n🌐 Potential team pages to check:")
                for page in team_pages[:5]:  # Show first 5
                    print(f"   {page}")

    print(f"\n💡 Tips:")
    print(f"   - Look for: UX Designer, Product Designer, Design Lead, Head of Design")
    print(f"   - Check their About page and Team page")
    print(f"   - Once you find contacts, use add_contact.py to add them to Contacts tab")

    # Show how to add contacts
    print(f"\n📝 To add a contact you find:")
    print(f'   python add_contact.py "Contact Name" --company "{company_name}" \\')
    print(f'     --tracker {tracker_type} --role "Job Title" --linkedin "profile_url"')


def find_all_contacts(tracker_type, region):
    """
    Find contacts for all companies needing research

    Args:
        tracker_type: Either 'fintech' or 'healthtech'
        region: Either 'new-england' or 'nyc'
    """
    print(f"\n🔍 Finding contacts for all companies in {tracker_type} tracker ({region})...")

    sheets = SheetsManager()

    # Get the appropriate sheet ID and tab
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return

    if region.lower() == 'new-england':
        sheet_name = config.NEW_ENGLAND_TAB
    elif region.lower() == 'nyc':
        sheet_name = config.NYC_TAB
    else:
        print("❌ Error: region must be 'new-england' or 'nyc'")
        return

    # Read all companies
    range_name = f"{sheet_name}!A:Z"
    data = sheets.read_sheet(sheet_id, range_name)

    if not data or len(data) < 2:
        print(f"No companies found in {sheet_name}")
        return

    # Find companies that need research
    # Column I (index 8) is Outreach Status
    companies_to_research = []
    for i, row in enumerate(data[1:], start=2):  # Skip header
        if row:
            company_name = row[0] if len(row) > 0 else ''
            status = row[8] if len(row) > 8 else ''

            # Look for companies that need research
            if company_name and status.lower() in ['to research', 'needs research', '']:
                companies_to_research.append(company_name)

    if not companies_to_research:
        print(f"✅ All companies in {sheet_name} have been researched!")
        return

    print(f"\n📋 Found {len(companies_to_research)} companies needing research:\n")

    for i, company in enumerate(companies_to_research, 1):
        print(f"{i}. {company}")

    print(f"\n💡 To research each company, run:")
    for company in companies_to_research[:3]:  # Show first 3 as examples
        print(f'   python find_contacts.py "{company}" --tracker {tracker_type} --region {region}')


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Find design team contacts for companies',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Research a specific company
  python find_contacts.py "Stripe" --tracker fintech --region new-england

  # Find all companies that need research in NYC
  python find_contacts.py --all --tracker healthtech --region nyc
        """
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
        '--region',
        choices=['new-england', 'nyc'],
        required=True,
        help='Which region tab to search in'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Show all companies that need research'
    )

    args = parser.parse_args()

    try:
        if args.all:
            find_all_contacts(args.tracker, args.region)
        elif args.company_name:
            find_contacts_for_company(args.company_name, args.tracker, args.region)
        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

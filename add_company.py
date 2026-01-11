#!/usr/bin/env python3
"""
Add Company Script
Add a new company to your networking tracker (New England or NYC regional tabs)

Usage:
    python add_company.py "Stripe" --tracker fintech --region new-england --location "San Francisco, CA"
    python add_company.py "Oscar Health" --tracker healthtech --region nyc --location "New York, NY"
"""

import argparse
import sys
from sheets_manager import SheetsManager
from company_researcher import CompanyResearcher
import config


def add_company(company_name, tracker_type, region, location='', focus_area='',
                ai_innovation='', company_size='', funding_stage=''):
    """
    Add a company to the specified tracker and region

    Args:
        company_name: Name of the company to add
        tracker_type: Either 'fintech' or 'healthtech'
        region: Either 'new-england' or 'nyc'
        location: City/state of company (optional)
        focus_area: What the company focuses on (optional)
        ai_innovation: AI/Innovation info (optional)
        company_size: Company size (startup, small, medium, large, enterprise)
        funding_stage: Funding stage (seed, series-a, series-b, etc.)
    """
    print(f"\n📋 Adding {company_name} to {tracker_type} tracker ({region})...")

    # Initialize managers
    sheets = SheetsManager()
    researcher = CompanyResearcher()

    # Get the appropriate sheet ID
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return False

    # Get the appropriate tab name
    if region.lower() == 'new-england':
        sheet_name = config.NEW_ENGLAND_TAB
    elif region.lower() == 'nyc':
        sheet_name = config.NYC_TAB
    else:
        print("❌ Error: region must be 'new-england' or 'nyc'")
        return False

    # Check if company already exists
    print("🔍 Checking if company already exists...")
    range_name = f"{sheet_name}!A:Z"
    existing_data = sheets.read_sheet(sheet_id, range_name)

    if existing_data:
        for row in existing_data[1:]:  # Skip header row
            if row and len(row) > 0 and row[0].lower() == company_name.lower():
                print(f"⚠️  {company_name} already exists in {sheet_name}!")
                return False

    # Create research template
    print("🔬 Creating research template...")
    research = researcher.create_company_research_template(company_name)

    # Prepare row data matching your column structure
    # Columns: Company | Location | Focus Area | AI/Innovation | Website/LinkedIn |
    #          Contact Name | Contact Role | Contact Info | Outreach Status | Next Steps | Notes |
    #          Company Size | Funding Stage
    new_row = [
        company_name,                           # A: Company
        location,                               # B: Location
        focus_area,                             # C: Focus Area
        ai_innovation,                          # D: AI/Innovation
        research.get('website', ''),            # E: Website/LinkedIn
        '',                                     # F: Contact Name
        '',                                     # G: Contact Role
        '',                                     # H: Contact Info
        'To Research',                          # I: Outreach Status
        'Find design contacts',                 # J: Next Steps
        'Added via automation',                 # K: Notes
        company_size.title() if company_size else '',  # L: Company Size
        funding_stage.title() if funding_stage else '' # M: Funding Stage
    ]

    # Add to sheet
    print("📝 Adding to Google Sheet...")
    result = sheets.append_row(sheet_id, f"{sheet_name}!A:M", new_row)

    if result:
        print(f"✅ Successfully added {company_name} to {sheet_name}!")
        print(f"\n📊 Next steps:")
        print(f"   1. Open your sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print(f"   2. Fill in the Website/LinkedIn column")
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
        description='Add a new company to your networking tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a fintech company in New England
  python add_company.py "Stripe" --tracker fintech --region new-england --location "San Francisco, CA"

  # Add a healthtech company in NYC
  python add_company.py "Oscar Health" --tracker healthtech --region nyc --location "New York, NY"

  # Add with more details
  python add_company.py "Ro" --tracker healthtech --region nyc \\
    --location "New York, NY" \\
    --focus-area "Digital pharmacy" \\
    --ai "Using AI for personalized healthcare"
        """
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
    parser.add_argument(
        '--region',
        choices=['new-england', 'nyc'],
        required=True,
        help='Which region tab to add to'
    )
    parser.add_argument(
        '--location',
        default='',
        help='City/state where company is located'
    )
    parser.add_argument(
        '--focus-area',
        default='',
        help='What the company focuses on'
    )
    parser.add_argument(
        '--ai',
        default='',
        help='AI/Innovation information'
    )
    parser.add_argument(
        '--size',
        choices=['startup', 'small', 'medium', 'large', 'enterprise'],
        default='',
        help='Company size (for filtering in sheets)'
    )
    parser.add_argument(
        '--funding',
        choices=['seed', 'series-a', 'series-b', 'series-c', 'series-d', 'series-e', 'series-f', 'public', 'acquired'],
        default='',
        help='Funding stage (for filtering in sheets)'
    )

    args = parser.parse_args()

    try:
        add_company(
            args.company_name,
            args.tracker,
            args.region,
            args.location,
            getattr(args, 'focus_area'),
            args.ai,
            args.size,
            args.funding
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

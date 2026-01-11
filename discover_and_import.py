#!/usr/bin/env python3
"""
Discover and Import Companies
Automatically discover companies and import them directly to your Google Sheets

Usage:
    # Import all suggested medium-sized fintech companies in Boston
    python discover_and_import.py --industry fintech --region boston --filter size=medium

    # Import Series B+ healthtech companies in NYC
    python discover_and_import.py --industry healthtech --region nyc --filter min_funding=series-b

    # Preview what would be imported (dry run)
    python discover_and_import.py --industry fintech --region boston --dry-run
"""

import argparse
import sys
from sheets_manager import SheetsManager
from discover_companies import CompanyDiscoverer
import config
import time


def discover_and_import(industry, region, tracker_type, filters=None, dry_run=False):
    """
    Discover companies and import them directly to Google Sheets

    Args:
        industry: Industry to search ('fintech' or 'healthtech')
        region: Region to search ('boston', 'nyc', 'sf')
        tracker_type: Which tracker to import to ('fintech' or 'healthtech')
        filters: Dict of filters (size, funding, etc.)
        dry_run: If True, just show what would be imported
    """
    print(f"\n🔍 Discovering {industry} companies in {region.upper()}...")

    # Initialize
    discoverer = CompanyDiscoverer()
    sheets = SheetsManager() if not dry_run else None

    # Get suggested companies with filters
    companies = discoverer.suggest_companies(industry, region, filters)

    if not companies:
        print("\n⚠️  No companies found matching your criteria")
        print("\n💡 Try:")
        print(f"   - Removing filters")
        print(f"   - Using a different region")
        return False

    # Display filter info
    filter_desc = ""
    if filters:
        filter_parts = [f"{k}={v}" for k, v in filters.items()]
        filter_desc = f" (filtered by: {', '.join(filter_parts)})"

    print(f"\n📋 Found {len(companies)} companies{filter_desc}")

    # Get sheet configuration
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return False

    # Map region to sheet tab
    region_map = {
        'boston': ('new-england', config.NEW_ENGLAND_TAB, 'Boston, MA'),
        'nyc': ('nyc', config.NYC_TAB, 'New York, NY'),
        'sf': ('new-england', config.NEW_ENGLAND_TAB, 'San Francisco, CA')
    }

    if region.lower() not in region_map:
        print(f"❌ Error: region must be 'boston', 'nyc', or 'sf'")
        return False

    region_key, sheet_name, default_location = region_map[region.lower()]

    # Get existing companies to avoid duplicates
    existing_companies = set()
    if not dry_run:
        print("🔍 Checking for existing companies...")
        range_name = f"{sheet_name}!A:Z"
        existing_data = sheets.read_sheet(sheet_id, range_name)

        if existing_data:
            for row in existing_data[1:]:  # Skip header
                if row and len(row) > 0:
                    existing_companies.add(row[0].lower())

    # Import companies
    added_count = 0
    skipped_count = 0

    print("\n" + "=" * 60)

    for i, company in enumerate(companies, 1):
        company_name = company['name']

        # Check if already exists
        if not dry_run and company_name.lower() in existing_companies:
            print(f"{i:2}. ⚠️  {company_name} - Already exists, skipping")
            skipped_count += 1
            continue

        # Prepare row data
        # Columns: Company | Location | Focus Area | AI/Innovation | Website/LinkedIn |
        #          Contact Name | Contact Role | Contact Info | Outreach Status | Next Steps | Notes |
        #          Company Size | Funding Stage
        new_row = [
            company_name,                                   # A: Company
            default_location,                               # B: Location
            company.get('focus', ''),                       # C: Focus Area
            '',                                             # D: AI/Innovation
            '',                                             # E: Website/LinkedIn
            '',                                             # F: Contact Name
            '',                                             # G: Contact Role
            '',                                             # H: Contact Info
            'To Research',                                  # I: Outreach Status
            'Find design contacts',                         # J: Next Steps
            'Auto-discovered',                              # K: Notes
            company.get('size', '').title(),               # L: Company Size
            company.get('funding', '').title()             # M: Funding Stage
        ]

        if dry_run:
            print(f"{i:2}. ✓ Would add: {company_name}")
            print(f"      Size: {company.get('size', 'unknown').title()} | Funding: {company.get('funding', 'unknown').title()}")
            if company.get('focus'):
                print(f"      Focus: {company.get('focus')}")
            added_count += 1
        else:
            # Add to sheet
            result = sheets.append_row(sheet_id, f"{sheet_name}!A:M", new_row)

            if result:
                print(f"{i:2}. ✅ Added: {company_name}")
                print(f"      Size: {company.get('size', '').title()} | Funding: {company.get('funding', '').title()}")
                added_count += 1
                existing_companies.add(company_name.lower())

                # Small delay to avoid rate limiting
                if i % 5 == 0:
                    time.sleep(0.3)
            else:
                print(f"{i:2}. ❌ Failed to add: {company_name}")

    # Summary
    print("\n" + "=" * 60)
    print(f"\n📊 Import Summary:")
    print(f"   ✅ Added: {added_count}")
    if skipped_count > 0:
        print(f"   ⚠️  Skipped (already exist): {skipped_count}")

    if dry_run:
        print(f"\n💡 This was a dry run. To actually import, remove --dry-run flag")
    else:
        print(f"\n🎉 Import complete!")
        print(f"   View your sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print(f"\n📝 Next steps:")
        print(f"   1. Open the Google Sheet and review the companies")
        print(f"   2. Add websites and focus areas for better context")
        print(f"   3. Use filtering in Google Sheets:")
        print(f"      - Filter by 'Company Size' column to see medium/large companies")
        print(f"      - Filter by 'Funding Stage' to prioritize well-funded companies")
        print(f"   4. Start researching:")
        print(f"      python find_contacts.py --all --tracker {tracker_type} --region {region_key}")

    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Discover and auto-import companies to Google Sheets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import all suggested medium-sized fintech companies in Boston
  python discover_and_import.py --industry fintech --region boston --filter size=medium

  # Import Series B+ healthtech companies in NYC
  python discover_and_import.py --industry healthtech --region nyc --filter min_funding=series-b

  # Import large/enterprise fintech companies in SF
  python discover_and_import.py --industry fintech --region sf --filter size=large

  # Preview what would be imported (dry run)
  python discover_and_import.py --industry fintech --region boston --dry-run

Filters:
  size=startup        Companies with 1-10 employees
  size=small          Companies with 11-50 employees
  size=medium         Companies with 51-200 employees
  size=large          Companies with 201-1000 employees
  size=enterprise     Companies with 1000+ employees

  funding=seed        Seed-stage companies
  funding=series-a    Series A companies
  funding=public      Public companies
  min_funding=series-b  Series B and beyond
        """
    )

    parser.add_argument(
        '--industry',
        choices=['fintech', 'healthtech'],
        required=True,
        help='Industry to search'
    )
    parser.add_argument(
        '--region',
        choices=['boston', 'nyc', 'sf'],
        required=True,
        help='Region to search'
    )
    parser.add_argument(
        '--tracker',
        choices=['fintech', 'healthtech'],
        help='Which tracker to import to (defaults to same as industry)'
    )
    parser.add_argument(
        '--filter',
        action='append',
        help='Apply filters (e.g., --filter size=medium --filter min_funding=series-a)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be imported without actually importing'
    )

    args = parser.parse_args()

    # Parse filters
    filters = {}
    if args.filter:
        for f in args.filter:
            if '=' in f:
                key, value = f.split('=', 1)
                filters[key] = value

    # Default tracker to same as industry
    tracker = args.tracker if args.tracker else args.industry

    try:
        discover_and_import(args.industry, args.region, tracker, filters, args.dry_run)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you have set up your credentials.json file!")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Import Companies Script
Batch import companies from a CSV file

CSV Format (comma-separated):
Company,Location,Focus Area,AI/Innovation,Website,Size,Funding

Example CSV content:
Stripe,San Francisco CA,Payment processing,Using AI for fraud detection,https://stripe.com,Enterprise,Series-H
Plaid,San Francisco CA,Financial data APIs,ML for transaction categorization,https://plaid.com,Large,Series-D

Usage:
    python import_companies.py companies.csv --tracker fintech --region new-england
    python import_companies.py healthtech_nyc.csv --tracker healthtech --region nyc --dry-run
"""

import argparse
import sys
import csv
from sheets_manager import SheetsManager
import config


def import_companies_from_csv(csv_file, tracker_type, region, dry_run=False):
    """
    Import companies from a CSV file

    Args:
        csv_file: Path to CSV file
        tracker_type: Either 'fintech' or 'healthtech'
        region: Either 'new-england' or 'nyc'
        dry_run: If True, just show what would be imported without actually importing
    """
    print(f"\n📂 Reading companies from {csv_file}...")

    # Initialize manager
    sheets = SheetsManager() if not dry_run else None

    # Get the appropriate sheet ID and tab
    if tracker_type.lower() == 'fintech':
        sheet_id = config.FINTECH_SHEET_ID
    elif tracker_type.lower() == 'healthtech':
        sheet_id = config.HEALTHTECH_SHEET_ID
    else:
        print("❌ Error: tracker_type must be 'fintech' or 'healthtech'")
        return False

    if region.lower() == 'new-england':
        sheet_name = config.NEW_ENGLAND_TAB
    elif region.lower() == 'nyc':
        sheet_name = config.NYC_TAB
    else:
        print("❌ Error: region must be 'new-england' or 'nyc'")
        return False

    # Read CSV file
    companies = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check for required column
            if 'Company' not in reader.fieldnames:
                print("❌ CSV must have at least a 'Company' column")
                print("   Expected columns: Company, Location, Focus Area, AI/Innovation, Website")
                return False

            for row in reader:
                companies.append(row)

    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
        return False
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False

    if not companies:
        print("⚠️  No companies found in CSV")
        return False

    print(f"✅ Found {len(companies)} companies in CSV")

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
    failed_count = 0

    print("\n" + "=" * 60)

    for i, company_data in enumerate(companies, 1):
        company_name = company_data.get('Company', '').strip()

        if not company_name:
            print(f"{i}. ⚠️  Skipping row with no company name")
            skipped_count += 1
            continue

        # Check if already exists
        if not dry_run and company_name.lower() in existing_companies:
            print(f"{i}. ⚠️  {company_name} - Already exists, skipping")
            skipped_count += 1
            continue

        # Prepare row data
        # Columns: Company | Location | Focus Area | AI/Innovation | Website/LinkedIn |
        #          Contact Name | Contact Role | Contact Info | Outreach Status | Next Steps | Notes |
        #          Company Size | Funding Stage
        new_row = [
            company_name,                                   # A: Company
            company_data.get('Location', ''),              # B: Location
            company_data.get('Focus Area', ''),            # C: Focus Area
            company_data.get('AI/Innovation', ''),         # D: AI/Innovation
            company_data.get('Website', ''),               # E: Website/LinkedIn
            '',                                             # F: Contact Name
            '',                                             # G: Contact Role
            '',                                             # H: Contact Info
            'To Research',                                  # I: Outreach Status
            'Find design contacts',                         # J: Next Steps
            'Imported via CSV',                             # K: Notes
            company_data.get('Size', ''),                  # L: Company Size
            company_data.get('Funding', '')                # M: Funding Stage
        ]

        if dry_run:
            print(f"{i}. ✓ Would add: {company_name}")
            if company_data.get('Location'):
                print(f"     Location: {company_data.get('Location')}")
            if company_data.get('Focus Area'):
                print(f"     Focus: {company_data.get('Focus Area')}")
            added_count += 1
        else:
            # Add to sheet
            result = sheets.append_row(sheet_id, f"{sheet_name}!A:M", new_row)

            if result:
                print(f"{i}. ✅ Added: {company_name}")
                added_count += 1
                existing_companies.add(company_name.lower())
            else:
                print(f"{i}. ❌ Failed to add: {company_name}")
                failed_count += 1

        # Small delay to avoid rate limiting
        if not dry_run and i % 10 == 0:
            time.sleep(0.5)

    # Summary
    print("\n" + "=" * 60)
    print(f"\n📊 Import Summary:")
    print(f"   ✅ Added: {added_count}")
    print(f"   ⚠️  Skipped: {skipped_count}")
    if failed_count > 0:
        print(f"   ❌ Failed: {failed_count}")

    if dry_run:
        print(f"\n💡 This was a dry run. To actually import, remove --dry-run flag")
    else:
        print(f"\n🎉 Import complete!")
        print(f"   View your sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print(f"\n📝 Next steps:")
        print(f"   1. Review the imported companies in your sheet")
        print(f"   2. Fill in any missing info (websites, focus areas)")
        print(f"   3. Use find_contacts.py to research design contacts")

    return True


def create_sample_csv():
    """Create a sample CSV file as a template"""
    sample_file = 'sample_companies.csv'

    sample_data = [
        ['Company', 'Location', 'Focus Area', 'AI/Innovation', 'Website', 'Size', 'Funding'],
        ['Stripe', 'San Francisco, CA', 'Payment processing', 'AI for fraud detection', 'https://stripe.com', 'Enterprise', 'Series-H'],
        ['Plaid', 'San Francisco, CA', 'Financial data APIs', 'ML for categorization', 'https://plaid.com', 'Large', 'Series-D'],
        ['Square', 'San Francisco, CA', 'Commerce platform', 'ML for lending', 'https://squareup.com', 'Enterprise', 'Public'],
    ]

    try:
        with open(sample_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)

        print(f"✅ Created sample CSV: {sample_file}")
        print(f"\n📋 Sample content:")
        for row in sample_data:
            print(f"   {','.join(row)}")

        return True
    except Exception as e:
        print(f"❌ Error creating sample: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Batch import companies from CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CSV Format:
  Required column: Company
  Optional columns: Location, Focus Area, AI/Innovation, Website

  Example CSV:
    Company,Location,Focus Area,Website
    Stripe,San Francisco CA,Payment processing,https://stripe.com
    Plaid,San Francisco CA,Financial APIs,https://plaid.com

Examples:
  # Create a sample CSV to see the format
  python import_companies.py --create-sample

  # Test import without actually adding (dry run)
  python import_companies.py companies.csv --tracker fintech --region new-england --dry-run

  # Actually import
  python import_companies.py companies.csv --tracker fintech --region new-england

  # Import healthtech companies to NYC
  python import_companies.py healthtech.csv --tracker healthtech --region nyc
        """
    )

    parser.add_argument(
        'csv_file',
        nargs='?',
        help='Path to CSV file with companies'
    )
    parser.add_argument(
        '--tracker',
        choices=['fintech', 'healthtech'],
        help='Which tracker to import to'
    )
    parser.add_argument(
        '--region',
        choices=['new-england', 'nyc'],
        help='Which region tab to import to'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be imported without actually importing'
    )
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Create a sample CSV file as a template'
    )

    args = parser.parse_args()

    try:
        if args.create_sample:
            create_sample_csv()
        elif args.csv_file and args.tracker and args.region:
            import time
            import_companies_from_csv(args.csv_file, args.tracker, args.region, args.dry_run)
        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

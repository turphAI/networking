#!/usr/bin/env python3
"""
Create a company research markdown file

Usage:
    python create_company_research.py "Company Name" --tracker fintech --region boston
    python create_company_research.py "Company Name" --from-sheet --tracker fintech --region new-england
"""

import argparse
import os
from datetime import datetime
from sheets_manager import SheetsManager
import config

def sanitize_filename(name):
    """Convert company name to safe filename"""
    # Remove special characters and replace spaces with underscores
    safe_name = "".join(c if c.isalnum() or c in (' ', '-') else '' for c in name)
    safe_name = safe_name.replace(' ', '_')
    return safe_name.lower()

def get_company_from_sheet(company_name, tracker_type, region):
    """Fetch company data from Google Sheet"""
    sheets = SheetsManager()

    # Get sheet ID based on tracker type
    sheet_id = config.FINTECH_SHEET_ID if tracker_type == 'fintech' else config.HEALTHTECH_SHEET_ID

    # Get tab name based on region
    if region in ['boston', 'new-england']:
        tab_name = config.NEW_ENGLAND_TAB
    elif region in ['nyc', 'new-york']:
        tab_name = config.NYC_TAB
    else:
        tab_name = config.NEW_ENGLAND_TAB

    # Read the sheet
    range_name = f"{tab_name}!A:M"
    rows = sheets.read_sheet(sheet_id, range_name)

    # Find the company
    for i, row in enumerate(rows):
        if i == 0:  # Skip header
            continue
        if row and row[0].lower() == company_name.lower():
            # Extract data (pad row with empty strings if needed)
            row = row + [''] * (13 - len(row))
            return {
                'company': row[0],
                'location': row[1],
                'focus_area': row[2],
                'ai_innovation': row[3],
                'website_linkedin': row[4],
                'contact_name': row[5],
                'contact_role': row[6],
                'contact_info': row[7],
                'outreach_status': row[8],
                'next_steps': row[9],
                'notes': row[10],
                'company_size': row[11],
                'funding_stage': row[12]
            }

    return None

def create_research_file(company_name, tracker_type, data=None):
    """Create a markdown research file for a company"""

    # Determine directory
    if tracker_type == 'fintech':
        directory = 'research/fintech'
    elif tracker_type == 'healthcare':
        directory = 'research/healthcare'
    else:
        directory = 'research'

    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Create filename
    filename = f"{sanitize_filename(company_name)}.md"
    filepath = os.path.join(directory, filename)

    # Check if file already exists
    if os.path.exists(filepath):
        print(f"⚠️  File already exists: {filepath}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    # Prepare data
    if data is None:
        data = {}

    # Read template
    template_path = 'research/TEMPLATE.md'
    with open(template_path, 'r') as f:
        template = f.read()

    # Replace placeholders
    content = template.format(
        company_name=data.get('company', company_name),
        industry=tracker_type.title(),
        location=data.get('location', ''),
        focus_area=data.get('focus_area', ''),
        company_size=data.get('company_size', ''),
        funding_stage=data.get('funding_stage', ''),
        website=data.get('website_linkedin', ''),
        linkedin=data.get('website_linkedin', ''),
        brief_description='',
        ai_innovation=data.get('ai_innovation', ''),
        outreach_status=data.get('outreach_status', 'Not contacted'),
        next_steps=data.get('next_steps', ''),
        notes=data.get('notes', ''),
        last_updated=datetime.now().strftime('%Y-%m-%d'),
        date=datetime.now().strftime('%Y-%m-%d')
    )

    # Write file
    with open(filepath, 'w') as f:
        f.write(content)

    print(f"✅ Created research file: {filepath}")
    print(f"\n📝 Open it with:")
    print(f"   open {filepath}")
    print(f"   # or")
    print(f"   code {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description='Create a company research markdown file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create from command line
  python create_company_research.py "Circle" --tracker fintech --region boston

  # Fetch data from Google Sheet
  python create_company_research.py "Circle" --from-sheet --tracker fintech --region new-england
        """
    )

    parser.add_argument('company_name', help='Name of the company')
    parser.add_argument('--tracker', choices=['fintech', 'healthcare'], required=True,
                        help='Which tracker (fintech or healthcare)')
    parser.add_argument('--region', choices=['boston', 'new-england', 'nyc', 'new-york'],
                        help='Region (for fetching from sheet)')
    parser.add_argument('--from-sheet', action='store_true',
                        help='Fetch company data from Google Sheet')

    args = parser.parse_args()

    data = None
    if args.from_sheet:
        if not args.region:
            print("❌ --region is required when using --from-sheet")
            return

        print(f"🔍 Fetching data for '{args.company_name}' from Google Sheet...")
        data = get_company_from_sheet(args.company_name, args.tracker, args.region)

        if data is None:
            print(f"⚠️  Company '{args.company_name}' not found in sheet")
            print("Creating empty research file...")
        else:
            print(f"✅ Found company data!")

    create_research_file(args.company_name, args.tracker, data)

if __name__ == '__main__':
    main()

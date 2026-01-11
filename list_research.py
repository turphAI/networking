#!/usr/bin/env python3
"""
List all company research files

Usage:
    python list_research.py
    python list_research.py --tracker fintech
    python list_research.py --search "series b"
"""

import argparse
import os
import re
from datetime import datetime

def extract_metadata(filepath):
    """Extract key metadata from markdown file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract company name (first h1)
        name_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        company_name = name_match.group(1) if name_match else os.path.basename(filepath).replace('.md', '')

        # Extract outreach status
        status_match = re.search(r'\*\*Outreach Status\*\*: (.+)$', content, re.MULTILINE)
        status = status_match.group(1) if status_match else 'Unknown'

        # Extract last updated
        updated_match = re.search(r'\*\*Last Updated\*\*: (.+)$', content, re.MULTILINE)
        last_updated = updated_match.group(1) if updated_match else 'Unknown'

        # Get file modification time as fallback
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        mod_time_str = mod_time.strftime('%Y-%m-%d')

        return {
            'name': company_name,
            'status': status.strip(),
            'last_updated': last_updated.strip(),
            'modified': mod_time_str,
            'path': filepath
        }
    except Exception as e:
        return {
            'name': os.path.basename(filepath).replace('.md', ''),
            'status': 'Error reading file',
            'last_updated': 'Unknown',
            'modified': 'Unknown',
            'path': filepath
        }

def list_research_files(tracker=None, search_term=None):
    """List all research markdown files"""

    # Determine directories to search
    if tracker:
        directories = [f'research/{tracker}']
    else:
        directories = ['research/fintech', 'research/healthcare']

    all_files = []

    for directory in directories:
        if not os.path.exists(directory):
            continue

        for filename in os.listdir(directory):
            if filename.endswith('.md') and filename != 'TEMPLATE.md':
                filepath = os.path.join(directory, filename)
                metadata = extract_metadata(filepath)

                # Filter by search term if provided
                if search_term:
                    with open(filepath, 'r') as f:
                        content = f.read().lower()
                    if search_term.lower() not in content:
                        continue

                metadata['tracker'] = directory.split('/')[-1]
                all_files.append(metadata)

    return all_files

def main():
    parser = argparse.ArgumentParser(description='List company research files')
    parser.add_argument('--tracker', choices=['fintech', 'healthcare'],
                        help='Filter by tracker type')
    parser.add_argument('--search', help='Search for term in files')
    parser.add_argument('--status', help='Filter by outreach status')

    args = parser.parse_args()

    print("📁 Company Research Files\n")

    files = list_research_files(args.tracker, args.search)

    # Filter by status if provided
    if args.status:
        files = [f for f in files if args.status.lower() in f['status'].lower()]

    if not files:
        print("No research files found.")
        return

    # Sort by modification date (most recent first)
    files.sort(key=lambda x: x['modified'], reverse=True)

    # Print header
    print(f"{'Company':<30} {'Tracker':<12} {'Status':<20} {'Last Modified':<15}")
    print("-" * 80)

    # Print files
    for f in files:
        company = f['name'][:28]
        tracker = f['tracker'][:10]
        status = f['status'][:18]
        modified = f['modified']

        print(f"{company:<30} {tracker:<12} {status:<20} {modified:<15}")

    print(f"\n📊 Total: {len(files)} files")

    if files:
        print(f"\n💡 To open a file:")
        print(f"   open {files[0]['path']}")
        print(f"   # or")
        print(f"   code {files[0]['path']}")

if __name__ == '__main__':
    main()

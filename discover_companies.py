#!/usr/bin/env python3
"""
Discover Companies Script
Search and discover companies to add to your networking tracker

This script helps you find companies from various sources:
- Web search results
- Company directories
- Manual lists

Usage:
    python discover_companies.py --search "fintech companies boston"
    python discover_companies.py --search "healthtech NYC" --limit 20
"""

import argparse
import sys
import requests
from bs4 import BeautifulSoup
import time


class CompanyDiscoverer:
    """Discover companies from various sources"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    def search_builtin(self, region, industry, limit=50):
        """
        Search Built In for companies

        Args:
            region: 'boston' or 'nyc'
            industry: 'fintech', 'healthtech', etc.
            limit: Max number of companies to find

        Returns:
            List of company dictionaries
        """
        print(f"\n🔍 Searching Built In {region.title()} for {industry} companies...")

        # Built In URLs
        builtin_urls = {
            'boston': 'https://builtin.com/companies/location/boston',
            'nyc': 'https://builtin.com/companies/location/new-york'
        }

        if region.lower() not in builtin_urls:
            print(f"❌ Region must be 'boston' or 'nyc'")
            return []

        # For now, return instructions for manual search
        # (Built In has anti-scraping measures, so manual approach is more reliable)

        print("\n📋 Manual Discovery Instructions:")
        print("=" * 60)
        print(f"\n1. Go to: {builtin_urls[region.lower()]}")
        print(f"2. Filter by industry: {industry}")
        print(f"3. Browse companies and note:")
        print("   - Company name")
        print("   - Location")
        print("   - What they do")
        print("   - Their website")
        print("\n4. Then add them using:")
        print(f"   python add_company.py 'Company Name' --tracker [fintech|healthtech] \\")

        region_map = {
            'boston': 'new-england',
            'nyc': 'nyc'
        }
        print(f"     --region {region_map.get(region.lower(), 'new-england')} --location 'City, State'")

        print("\n💡 Or use import_companies.py to batch import from a CSV")

        return []

    def generate_search_urls(self, industry, region):
        """
        Generate useful search URLs for finding companies

        Args:
            industry: 'fintech', 'healthtech', etc.
            region: 'boston', 'nyc', etc.

        Returns:
            Dictionary of search URLs
        """
        urls = {
            'Built In': f'https://builtin.com/companies?location={region}&industry={industry}',
            'Crunchbase': f'https://www.crunchbase.com/discover/organization.companies/{industry}%20{region}',
            'AngelList': f'https://angel.co/company-filters?locations=1986-{region}&markets={industry}',
            'Google': f'https://www.google.com/search?q={industry}+companies+in+{region}',
        }

        return urls

    def suggest_companies(self, industry, region):
        """
        Suggest well-known companies to research

        Args:
            industry: 'fintech' or 'healthtech'
            region: 'boston', 'nyc', etc.
        """
        suggestions = {
            'fintech': {
                'boston': [
                    'Circle', 'Toast', 'Flywire', 'Vestmark', 'Acacia',
                    'Cybereason', 'DraftKings', 'Klaviyo', 'Wayfair'
                ],
                'nyc': [
                    'Stripe', 'Plaid', 'Better', 'Ramp', 'Brex',
                    'Carta', 'Chime', 'Robinhood', 'Square', 'Affirm'
                ],
                'sf': [
                    'Stripe', 'Plaid', 'Chime', 'Brex', 'Ramp',
                    'Affirm', 'Square', 'Robinhood', 'Coinbase'
                ]
            },
            'healthtech': {
                'boston': [
                    'Flatiron Health', 'Kyruus', 'OM1', 'Zocdoc', 'Included Health',
                    'Cedar', 'Rightway', 'Devoted Health', 'Ro'
                ],
                'nyc': [
                    'Oscar Health', 'Zocdoc', 'Ro', 'Hims & Hers', 'Spring Health',
                    'Headway', 'Cedar', 'K Health', 'Cityblock Health'
                ],
                'sf': [
                    'Oscar Health', 'Devoted Health', 'Omada Health', 'Livongo',
                    'One Medical', 'Ro', 'Hims & Hers', 'Ginger'
                ]
            }
        }

        industry_lower = industry.lower()
        region_lower = region.lower()

        if industry_lower in suggestions and region_lower in suggestions[industry_lower]:
            return suggestions[industry_lower][region_lower]

        return []


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Discover companies for your networking tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get discovery resources for fintech in Boston
  python discover_companies.py --industry fintech --region boston

  # Get healthtech companies in NYC
  python discover_companies.py --industry healthtech --region nyc

  # See well-known companies to add
  python discover_companies.py --industry fintech --region boston --suggest
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
        '--suggest',
        action='store_true',
        help='Show suggested well-known companies to add'
    )
    parser.add_argument(
        '--urls',
        action='store_true',
        help='Generate search URLs for finding companies'
    )

    args = parser.parse_args()

    discoverer = CompanyDiscoverer()

    try:
        # Show suggested companies
        if args.suggest:
            suggestions = discoverer.suggest_companies(args.industry, args.region)

            if suggestions:
                print(f"\n📋 Well-known {args.industry} companies in {args.region.upper()}:")
                print("=" * 60)
                for i, company in enumerate(suggestions, 1):
                    print(f"{i:2}. {company}")

                print(f"\n💡 To add these companies:")

                region_map = {
                    'boston': 'new-england',
                    'nyc': 'nyc',
                    'sf': 'new-england'  # or create a new tab
                }

                tracker = args.industry
                region = region_map.get(args.region, 'new-england')

                print(f"\n   python add_company.py 'Company Name' --tracker {tracker} --region {region} \\")
                print(f"     --location '{args.region.title()}, [State]'")

                print(f"\n   Example:")
                if suggestions:
                    print(f"   python add_company.py '{suggestions[0]}' --tracker {tracker} --region {region} \\")
                    print(f"     --location '{args.region.title()}, MA'")
            else:
                print(f"\n⚠️  No suggestions available for {args.industry} in {args.region}")

        # Show search URLs
        if args.urls or not args.suggest:
            urls = discoverer.generate_search_urls(args.industry, args.region)

            print(f"\n🔗 Search URLs for {args.industry} companies in {args.region.upper()}:")
            print("=" * 60)
            for source, url in urls.items():
                print(f"\n{source}:")
                print(f"  {url}")

            print("\n💡 Browse these sites to discover companies, then add them with:")
            print("   python add_company.py 'Company Name' --tracker [fintech|healthtech] \\")
            print("     --region [new-england|nyc] --location 'City, State'")

        # Instructions for batch import
        print("\n" + "=" * 60)
        print("\n📝 Pro tip: Create a list of companies, then use batch import!")
        print("   Create a CSV with columns: Company,Location,Focus Area")
        print("   Then run: python import_companies.py companies.csv --tracker fintech --region nyc")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

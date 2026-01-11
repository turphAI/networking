#!/usr/bin/env python3
"""
Discover Companies Script
Search and discover companies from multiple sources with filtering

Data sources:
- Y Combinator directory (scrapable)
- Built In (Boston/NYC)
- Crunchbase searches
- Wellfound/AngelList
- Google searches

Usage:
    python discover_companies.py --industry fintech --region boston --suggest
    python discover_companies.py --industry healthtech --region nyc --source yc
    python discover_companies.py --industry fintech --region boston --filter size:medium funding:series-a
"""

import argparse
import sys
import requests
from bs4 import BeautifulSoup
import time
import json


class CompanyDiscoverer:
    """Discover companies from various sources"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def search_yc_directory(self, industry_keywords, region_keywords=None, filters=None):
        """
        Search Y Combinator company directory

        Args:
            industry_keywords: Keywords to search (e.g., ['fintech', 'payments'])
            region_keywords: Location keywords (e.g., ['boston', 'massachusetts'])
            filters: Dict of filters (size, funding, etc.)

        Returns:
            List of company dictionaries
        """
        print(f"\n🔍 Searching Y Combinator directory...")

        # YC directory URL
        yc_url = "https://www.ycombinator.com/companies"

        try:
            # For now, provide instructions for manual search
            # (YC has anti-bot measures, but their directory is searchable)
            print(f"\n📋 Y Combinator Search Instructions:")
            print("=" * 60)
            print(f"\n1. Visit: {yc_url}")
            print(f"2. Use filters:")
            if industry_keywords:
                print(f"   - Industry: {', '.join(industry_keywords)}")
            if region_keywords:
                print(f"   - Region: {', '.join(region_keywords)}")
            if filters:
                if 'batch' in filters:
                    print(f"   - Batch: {filters['batch']} (e.g., W24, S23)")
                if 'size' in filters:
                    print(f"   - Team size: {filters['size']}")

            print(f"\n3. Browse results and export companies")
            print(f"\n💡 Pro tip: YC companies often have strong design cultures!")

            # Suggest some well-known YC companies
            yc_suggestions = self._get_yc_companies_by_industry(industry_keywords)
            if yc_suggestions:
                print(f"\n🌟 Well-known YC {industry_keywords[0] if industry_keywords else ''} companies:")
                for company in yc_suggestions[:10]:
                    print(f"   - {company}")

            return []

        except Exception as e:
            print(f"⚠️  Error accessing YC directory: {e}")
            return []

    def _get_yc_companies_by_industry(self, keywords):
        """Get curated list of YC companies by industry"""
        yc_companies = {
            'fintech': [
                'Stripe', 'Plaid', 'Brex', 'Ramp', 'Mercury', 'Gusto',
                'Lattice', 'Rippling', 'Deel', 'Checkr', 'Affin', 'Arc'
            ],
            'healthtech': [
                'Ro', 'Hims & Hers', 'Cityblock Health', 'Carbon Health',
                'Forward', 'Calibrate', 'K Health', 'Headway', 'Tia'
            ],
            'payments': ['Stripe', 'Brex', 'Ramp', 'Mercury', 'Plaid'],
            'b2b': ['Lattice', 'Rippling', 'Deel', 'Gusto', 'Ramp'],
            'healthcare': ['Ro', 'Carbon Health', 'Forward', 'Cityblock Health']
        }

        results = set()
        if keywords:
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in yc_companies:
                    results.update(yc_companies[keyword_lower])

        return list(results)

    def search_wellfound(self, industry, region, filters=None):
        """
        Generate Wellfound (AngelList) search URLs

        Args:
            industry: Industry tag
            region: Location
            filters: Dict of filters (size, funding, etc.)
        """
        print(f"\n🔍 Generating Wellfound/AngelList search...")

        # Build search URL
        base_url = "https://wellfound.com/jobs"

        # Map regions to Wellfound location IDs
        location_map = {
            'boston': 'boston',
            'nyc': 'new-york-city',
            'sf': 'san-francisco',
            'remote': 'remote'
        }

        location = location_map.get(region.lower(), region)

        # Build URL with filters
        params = []
        params.append(f"locations[]={location}")

        # Add role filter for designers
        params.append("role=Design")

        # Add industry/market filters
        industry_tags = {
            'fintech': ['fintech', 'payments', 'banking', 'finance'],
            'healthtech': ['health-tech', 'healthcare', 'digital-health']
        }

        if industry.lower() in industry_tags:
            for tag in industry_tags[industry.lower()]:
                params.append(f"markets[]={tag}")

        # Add size filter
        if filters and 'size' in filters:
            size_map = {
                'startup': '1-10',
                'small': '11-50',
                'medium': '51-200',
                'large': '201-1000',
                'enterprise': '1001+'
            }
            if filters['size'] in size_map:
                params.append(f"company_size[]={size_map[filters['size']]}")

        # Add funding filter
        if filters and 'funding' in filters:
            funding_map = {
                'seed': 'seed',
                'series-a': 'series-a',
                'series-b': 'series-b',
                'series-c': 'series-c+'
            }
            if filters['funding'] in funding_map:
                params.append(f"stage[]={funding_map[filters['funding']]}")

        url = f"{base_url}?{'&'.join(params)}"

        print(f"\n🔗 Wellfound Search URL:")
        print(f"   {url}")
        print(f"\n💡 This shows design roles at {industry} companies in {region}")
        print(f"   Click on companies to learn more about them")

        return url

    def search_crunchbase(self, industry, region, filters=None):
        """
        Generate Crunchbase search URL

        Args:
            industry: Industry category
            region: Location
            filters: Dict of filters
        """
        print(f"\n🔍 Generating Crunchbase search...")

        base_url = "https://www.crunchbase.com/discover/organization.companies"

        # Crunchbase has advanced search - generate URL
        industry_map = {
            'fintech': 'financial-services',
            'healthtech': 'health-care'
        }

        category = industry_map.get(industry.lower(), industry)

        print(f"\n🔗 Crunchbase Search:")
        print(f"   {base_url}")
        print(f"\n📋 Recommended filters:")
        print(f"   - Categories: {category}")
        print(f"   - Location: {region.title()}")

        if filters:
            print(f"   - Filters:")
            if 'funding' in filters:
                print(f"     * Funding: {filters['funding']}")
            if 'size' in filters:
                print(f"     * Company size: {filters['size']}")
            if 'founded' in filters:
                print(f"     * Founded after: {filters['founded']}")

        print(f"\n💡 Note: Crunchbase requires account for advanced filtering")

        return base_url

    def generate_search_urls(self, industry, region, filters=None):
        """
        Generate comprehensive search URLs from all sources

        Args:
            industry: Industry to search
            region: Region to search
            filters: Optional filters dict

        Returns:
            Dict of search URLs
        """
        urls = {}

        # Built In
        builtin_map = {
            'boston': f'https://builtin.com/companies?location=boston&industries={industry}',
            'nyc': f'https://builtin.com/companies?location=new-york&industries={industry}',
            'sf': f'https://builtin.com/companies?location=san-francisco&industries={industry}'
        }
        if region.lower() in builtin_map:
            urls['Built In'] = builtin_map[region.lower()]

        # Y Combinator
        urls['Y Combinator'] = 'https://www.ycombinator.com/companies'

        # Wellfound
        urls['Wellfound'] = self.search_wellfound(industry, region, filters)

        # Crunchbase
        urls['Crunchbase'] = self.search_crunchbase(industry, region, filters)

        # LinkedIn
        linkedin_search = f'https://www.linkedin.com/search/results/companies/?keywords={industry}%20{region}'
        urls['LinkedIn Companies'] = linkedin_search

        # Google
        google_query = f'{industry} companies {region}'
        if filters and 'size' in filters:
            google_query += f' {filters["size"]}'
        urls['Google'] = f'https://www.google.com/search?q={google_query.replace(" ", "+")}'

        return urls

    def suggest_companies(self, industry, region, filters=None):
        """
        Suggest well-known companies with filtering

        Args:
            industry: 'fintech' or 'healthtech'
            region: 'boston', 'nyc', 'sf', etc.
            filters: Dict of filters (size, funding, etc.)
        """
        all_suggestions = {
            'fintech': {
                'boston': [
                    {'name': 'Circle', 'size': 'medium', 'funding': 'series-d', 'focus': 'Crypto payments'},
                    {'name': 'Toast', 'size': 'large', 'funding': 'public', 'focus': 'Restaurant tech'},
                    {'name': 'Flywire', 'size': 'large', 'funding': 'public', 'focus': 'Global payments'},
                    {'name': 'Vestmark', 'size': 'medium', 'funding': 'private', 'focus': 'Wealth management'},
                    {'name': 'DraftKings', 'size': 'enterprise', 'funding': 'public', 'focus': 'Sports betting'},
                    {'name': 'Klaviyo', 'size': 'large', 'funding': 'public', 'focus': 'Marketing automation'},
                    {'name': 'Acacia', 'size': 'small', 'funding': 'series-a', 'focus': 'SMB lending'},
                    {'name': 'Carta', 'size': 'large', 'funding': 'series-f', 'focus': 'Equity management'},
                ],
                'nyc': [
                    {'name': 'Stripe', 'size': 'enterprise', 'funding': 'series-h', 'focus': 'Payments infrastructure'},
                    {'name': 'Plaid', 'size': 'large', 'funding': 'series-d', 'focus': 'Financial data'},
                    {'name': 'Ramp', 'size': 'medium', 'funding': 'series-d', 'focus': 'Corporate cards'},
                    {'name': 'Brex', 'size': 'medium', 'funding': 'series-d', 'focus': 'Corporate cards'},
                    {'name': 'Carta', 'size': 'large', 'funding': 'series-f', 'focus': 'Equity management'},
                    {'name': 'Better', 'size': 'medium', 'funding': 'series-e', 'focus': 'Mortgage'},
                    {'name': 'Affirm', 'size': 'large', 'funding': 'public', 'focus': 'BNPL'},
                    {'name': 'Robinhood', 'size': 'large', 'funding': 'public', 'focus': 'Trading'},
                ],
                'sf': [
                    {'name': 'Stripe', 'size': 'enterprise', 'funding': 'series-h', 'focus': 'Payments'},
                    {'name': 'Plaid', 'size': 'large', 'funding': 'series-d', 'focus': 'Financial APIs'},
                    {'name': 'Chime', 'size': 'large', 'funding': 'series-g', 'focus': 'Digital banking'},
                    {'name': 'Square', 'size': 'enterprise', 'funding': 'public', 'focus': 'Commerce'},
                    {'name': 'Coinbase', 'size': 'enterprise', 'funding': 'public', 'focus': 'Crypto'},
                    {'name': 'Mercury', 'size': 'small', 'funding': 'series-b', 'focus': 'Business banking'},
                ]
            },
            'healthtech': {
                'boston': [
                    {'name': 'Flatiron Health', 'size': 'large', 'funding': 'acquired', 'focus': 'Oncology data'},
                    {'name': 'Kyruus', 'size': 'medium', 'funding': 'series-e', 'focus': 'Provider search'},
                    {'name': 'OM1', 'size': 'medium', 'funding': 'series-c', 'focus': 'Healthcare data'},
                    {'name': 'Devoted Health', 'size': 'large', 'funding': 'series-e', 'focus': 'Medicare Advantage'},
                    {'name': 'Included Health', 'size': 'large', 'funding': 'series-e', 'focus': 'Virtual care'},
                ],
                'nyc': [
                    {'name': 'Oscar Health', 'size': 'large', 'funding': 'public', 'focus': 'Health insurance'},
                    {'name': 'Zocdoc', 'size': 'medium', 'funding': 'series-d', 'focus': 'Doctor booking'},
                    {'name': 'Ro', 'size': 'medium', 'funding': 'series-d', 'focus': 'Telehealth'},
                    {'name': 'Hims & Hers', 'size': 'large', 'funding': 'public', 'focus': 'Telehealth'},
                    {'name': 'Spring Health', 'size': 'medium', 'funding': 'series-e', 'focus': 'Mental health'},
                    {'name': 'Headway', 'size': 'small', 'funding': 'series-c', 'focus': 'Mental health'},
                    {'name': 'Cedar', 'size': 'medium', 'funding': 'series-d', 'focus': 'Patient billing'},
                ],
                'sf': [
                    {'name': 'One Medical', 'size': 'large', 'funding': 'acquired', 'focus': 'Primary care'},
                    {'name': 'Omada Health', 'size': 'medium', 'funding': 'series-e', 'focus': 'Chronic care'},
                    {'name': 'Livongo', 'size': 'large', 'funding': 'acquired', 'focus': 'Diabetes care'},
                    {'name': 'Ginger', 'size': 'small', 'funding': 'series-e', 'focus': 'Mental health'},
                ]
            }
        }

        industry_lower = industry.lower()
        region_lower = region.lower()

        if industry_lower not in all_suggestions:
            return []

        if region_lower not in all_suggestions[industry_lower]:
            return []

        companies = all_suggestions[industry_lower][region_lower]

        # Apply filters
        if filters:
            filtered = companies

            if 'size' in filters:
                filtered = [c for c in filtered if c.get('size') == filters['size']]

            if 'funding' in filters:
                filtered = [c for c in filtered if filters['funding'] in c.get('funding', '')]

            if 'min_funding' in filters:
                # Filter by minimum funding stage
                funding_order = ['seed', 'series-a', 'series-b', 'series-c', 'series-d', 'series-e', 'series-f', 'public']
                min_stage = filters['min_funding']
                if min_stage in funding_order:
                    min_index = funding_order.index(min_stage)
                    filtered = [c for c in filtered
                               if any(stage in c.get('funding', '') for stage in funding_order[min_index:])]

            return filtered

        return companies


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Discover companies from multiple sources with filtering',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get suggested companies
  python discover_companies.py --industry fintech --region boston --suggest

  # Filter by size
  python discover_companies.py --industry fintech --region nyc --suggest --filter size=medium

  # Filter by funding stage
  python discover_companies.py --industry healthtech --region boston --suggest --filter min_funding=series-b

  # Get search URLs for all sources
  python discover_companies.py --industry fintech --region nyc --urls

  # Search Y Combinator directory
  python discover_companies.py --industry fintech --source yc

Filters:
  size: startup, small, medium, large, enterprise
  funding: seed, series-a, series-b, series-c, series-d, public
  min_funding: series-a (shows companies at series-a and beyond)
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
        help='Show suggested well-known companies'
    )
    parser.add_argument(
        '--urls',
        action='store_true',
        help='Generate search URLs for all sources'
    )
    parser.add_argument(
        '--source',
        choices=['yc', 'wellfound', 'crunchbase', 'builtin'],
        help='Search specific source'
    )
    parser.add_argument(
        '--filter',
        action='append',
        help='Apply filters (e.g., --filter size=medium --filter min_funding=series-a)'
    )

    args = parser.parse_args()

    # Parse filters
    filters = {}
    if args.filter:
        for f in args.filter:
            if '=' in f:
                key, value = f.split('=', 1)
                filters[key] = value

    discoverer = CompanyDiscoverer()

    try:
        # Search specific source
        if args.source == 'yc':
            industry_keywords = [args.industry]
            region_keywords = [args.region]
            discoverer.search_yc_directory(industry_keywords, region_keywords, filters)

        elif args.source == 'wellfound':
            discoverer.search_wellfound(args.industry, args.region, filters)

        elif args.source == 'crunchbase':
            discoverer.search_crunchbase(args.industry, args.region, filters)

        # Show suggested companies
        elif args.suggest or (not args.urls and not args.source):
            suggestions = discoverer.suggest_companies(args.industry, args.region, filters)

            if suggestions:
                filter_desc = ""
                if filters:
                    filter_parts = [f"{k}={v}" for k, v in filters.items()]
                    filter_desc = f" (filtered by: {', '.join(filter_parts)})"

                print(f"\n📋 {args.industry.title()} companies in {args.region.upper()}{filter_desc}:")
                print("=" * 60)

                for i, company in enumerate(suggestions, 1):
                    name = company['name']
                    size = company.get('size', 'unknown')
                    funding = company.get('funding', 'unknown')
                    focus = company.get('focus', '')

                    print(f"\n{i:2}. {name}")
                    print(f"    Size: {size.title()} | Funding: {funding.title()}")
                    if focus:
                        print(f"    Focus: {focus}")

                print(f"\n💡 To add these companies:")
                region_map = {
                    'boston': 'new-england',
                    'nyc': 'nyc',
                    'sf': 'new-england'
                }

                tracker = args.industry
                region = region_map.get(args.region, 'new-england')

                if suggestions:
                    print(f"\n   python add_company.py '{suggestions[0]['name']}' --tracker {tracker} --region {region} \\")
                    print(f"     --location '{args.region.title()}, [State]' \\")
                    print(f"     --focus-area '{suggestions[0].get('focus', '')}}'")
            else:
                print(f"\n⚠️  No companies match your filters")

        # Show search URLs
        if args.urls:
            urls = discoverer.generate_search_urls(args.industry, args.region, filters)

            print(f"\n🔗 Search URLs for {args.industry} companies in {args.region.upper()}:")
            print("=" * 60)

            for source, url in urls.items():
                print(f"\n{source}:")
                print(f"  {url}")

        # Show all if no specific action
        if not args.suggest and not args.urls and not args.source:
            print(f"\nℹ️  Use --suggest to see company suggestions or --urls for search links")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

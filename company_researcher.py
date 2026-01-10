"""
Company Researcher
Helps find design team contacts at companies
"""

import requests
from bs4 import BeautifulSoup
import time


class CompanyResearcher:
    """Research companies and find design team contacts"""

    def __init__(self):
        """Initialize the researcher"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def search_company_website(self, company_name):
        """
        Search for a company's website

        Args:
            company_name: Name of the company to search for

        Returns:
            Dictionary with company information (website, etc.)
        """
        # This is a simplified version. In production, you might want to use:
        # - Google Custom Search API
        # - Clearbit API
        # - Other company data APIs

        print(f"Searching for {company_name}...")

        # For now, return a template that the user can fill in manually
        return {
            'company_name': company_name,
            'website': '',  # User will need to add this
            'linkedin': '',  # User will need to add this
            'status': 'needs_research'
        }

    def find_design_team_page(self, website):
        """
        Try to find the design team or about page on a company website

        Args:
            website: Company website URL

        Returns:
            List of potential pages to check for design team info
        """
        if not website or not website.startswith('http'):
            return []

        common_paths = [
            '/team',
            '/about',
            '/about-us',
            '/people',
            '/design',
            '/designers',
            '/our-team',
            '/leadership',
            '/careers'
        ]

        potential_pages = []

        for path in common_paths:
            url = website.rstrip('/') + path
            potential_pages.append(url)

        return potential_pages

    def extract_contacts_from_linkedin(self, company_name):
        """
        Extract design contacts from LinkedIn

        NOTE: This is a placeholder function. LinkedIn's terms of service
        don't allow automated scraping. Instead, you should:

        1. Manually search on LinkedIn: "[Company Name] UX Designer"
        2. Filter by company
        3. Find relevant contacts
        4. Use the update_contact script to add them to your sheet

        Args:
            company_name: Name of the company

        Returns:
            Instructions for manual research
        """
        linkedin_search_url = f"https://www.linkedin.com/search/results/people/?keywords={company_name.replace(' ', '%20')}%20ux%20designer"

        return {
            'manual_search_required': True,
            'search_url': linkedin_search_url,
            'instructions': [
                f"1. Open this URL: {linkedin_search_url}",
                "2. Add company filter on the left sidebar",
                "3. Look for roles like: UX Designer, Product Designer, Design Lead, Head of Design",
                "4. Note down their names and titles",
                "5. Use the update_contact script to add them to your sheet"
            ]
        }

    def create_company_research_template(self, company_name):
        """
        Create a research template for a company

        Args:
            company_name: Name of the company

        Returns:
            Dictionary with research template
        """
        website_info = self.search_company_website(company_name)
        linkedin_info = self.extract_contacts_from_linkedin(company_name)

        return {
            'company_name': company_name,
            'website': website_info.get('website', ''),
            'linkedin_company': f"https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}/",
            'linkedin_search': linkedin_info['search_url'],
            'status': 'To Research',
            'notes': 'Added for research',
            'research_steps': linkedin_info['instructions']
        }


def main():
    """Test the researcher"""
    researcher = CompanyResearcher()

    # Test with a company
    test_company = "Stripe"
    result = researcher.create_company_research_template(test_company)

    print("\nCompany Research Template:")
    print("=" * 50)
    for key, value in result.items():
        if key != 'research_steps':
            print(f"{key}: {value}")

    print("\nResearch Steps:")
    for step in result['research_steps']:
        print(f"  {step}")


if __name__ == "__main__":
    main()

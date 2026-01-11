"""
Configuration file for networking tracker
Loads settings from .env file if present, otherwise uses defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Your Google Sheet IDs (the long string in the URL)
# These can be set in .env file or use the defaults below
FINTECH_SHEET_ID = os.getenv('FINTECH_SHEET_ID', '1Ir2nA37z9iNxVCKHbhSSNK_VJsI49f6N')
HEALTHTECH_SHEET_ID = os.getenv('HEALTHTECH_SHEET_ID', '1Y4djqEJoGqLuxLaMlDpa5DKjkWl3Zhf9')

# Tab names within each spreadsheet
# Both Fintech and HealthTech have the same tab structure
CONTACTS_TAB = 'Contacts'
NEW_ENGLAND_TAB = 'New England'
NYC_TAB = 'NYC'
ORGANIZATION_TAB = 'Organization'

# Column mappings for Contacts tab
# Columns: Company | Name | Role/Title | LinkedIn Profile | Background Notes | Contact Status | Last Outreach | Notes
CONTACTS_COLUMNS = {
    'company': 'A',
    'name': 'B',
    'role': 'C',
    'linkedin': 'D',
    'background': 'E',
    'status': 'F',
    'last_outreach': 'G',
    'notes': 'H'
}

# Column mappings for New England and NYC tabs
# Columns: Company | Location | Focus Area | AI/Innovation | Website/LinkedIn |
#          Contact Name | Contact Role | Contact Info | Outreach Status | Next Steps | Notes |
#          Company Size | Funding Stage
COMPANY_COLUMNS = {
    'company': 'A',
    'location': 'B',
    'focus_area': 'C',
    'ai_innovation': 'D',
    'website_linkedin': 'E',
    'contact_name': 'F',
    'contact_role': 'G',
    'contact_info': 'H',
    'outreach_status': 'I',
    'next_steps': 'J',
    'notes': 'K',
    'company_size': 'L',      # NEW: For filtering by company size
    'funding_stage': 'M'       # NEW: For filtering by funding stage
}

# Column mappings for Organization tab
# Columns: Organization/Event | Location | Type | Description | Timing/Frequency | Contact/Website | Notes
ORGANIZATION_COLUMNS = {
    'organization': 'A',
    'location': 'B',
    'type': 'C',
    'description': 'D',
    'timing': 'E',
    'contact_website': 'F',
    'notes': 'G'
}

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

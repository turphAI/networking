# Quick Start Guide

Your sheets have 4 tabs. Here's how to use them:

## Your Sheet Structure

Both Fintech and HealthTech have:
1. **Contacts** - Individual design contacts (main networking tab)
2. **New England** - Companies in New England
3. **NYC** - Companies in NYC
4. **Organization** - Networking events and organizations

## Common Workflows

### Workflow 1: Add and Research a Company

```bash
# 1. Add company
python add_company.py "Stripe" --tracker fintech --region new-england --location "San Francisco, CA"

# 2. Research contacts
python find_contacts.py "Stripe" --tracker fintech --region new-england

# 3. Add contact you found
python add_contact.py "Jane Doe" --company "Stripe" --tracker fintech \
  --role "Senior UX Designer" --linkedin "https://linkedin.com/in/janedoe"

# 4. Track outreach
python update_contact.py "Jane Doe" --company "Stripe" --tracker fintech \
  --status "Reached Out" --notes "Sent message on 1/10"
```

### Workflow 2: Add an Organization

```bash
python add_organization.py "UXPA Boston" --tracker fintech \
  --location "Boston, MA" --type "Professional Organization" \
  --contact "https://uxpaboston.org"
```

### Workflow 3: Auto-Discover and Import Companies (NEW!)

```bash
# Discover and import medium-sized fintech companies in Boston
python discover_and_import.py --industry fintech --region boston --filter size=medium

# Import Series B+ healthtech companies in NYC
python discover_and_import.py --industry healthtech --region nyc --filter min_funding=series-b

# Preview first (dry run)
python discover_and_import.py --industry fintech --region boston --dry-run
```

**What this does:**
- Finds curated companies matching your filters
- Automatically adds them to your Google Sheet
- Includes metadata (size, funding) for filtering in Google Sheets

**Then filter in Google Sheets:**
- Click "Create a filter" button in sheets
- Filter by "Company Size" column → Select "Medium" or "Large"
- Filter by "Funding Stage" → Select "Series-B", "Series-C", etc.
- Prioritize which companies to research based on these attributes

## Command Reference

### Companies (New England & NYC tabs)

```bash
# Add
python add_company.py "Name" --tracker [fintech|healthtech] \
  --region [new-england|nyc] --location "City, State"

# Research
python find_contacts.py "Name" --tracker [fintech|healthtech] \
  --region [new-england|nyc]

# List all needing research
python find_contacts.py --all --tracker [fintech|healthtech] \
  --region [new-england|nyc]
```

### Contacts (Contacts tab)

```bash
# Add
python add_contact.py "Name" --company "Company" --tracker [fintech|healthtech] \
  --role "Job Title" --linkedin "URL"

# Update status
python update_contact.py "Name" --company "Company" --tracker [fintech|healthtech] \
  --status "Reached Out"

# View info
python update_contact.py "Name" --company "Company" --tracker [fintech|healthtech] --show
```

### Organizations (Organization tab)

```bash
python add_organization.py "Name" --tracker [fintech|healthtech] \
  --location "Location" --type "Type"
```

## Status Values

**Contacts:**
- Not Contacted
- Reached Out
- Responded
- Meeting Scheduled
- Follow Up
- Not Interested

**Companies:**
- To Research
- Researching
- Contacted
- In Progress

## Example Session

```bash
# Morning: Add companies
python add_company.py "Plaid" --tracker fintech --region new-england --location "SF, CA"

# Afternoon: Research
python find_contacts.py "Plaid" --tracker fintech --region new-england
# [Search LinkedIn manually]
python add_contact.py "Sarah Lee" --company "Plaid" --tracker fintech \
  --role "Design Lead" --linkedin "https://linkedin.com/in/sarahlee"

# Evening: Reach out
python update_contact.py "Sarah Lee" --company "Plaid" --tracker fintech \
  --status "Reached Out" --notes "Sent InMail"

# Next day: They responded!
python update_contact.py "Sarah Lee" --company "Plaid" --tracker fintech \
  --status "Responded" --notes "Scheduling call"
```

## Full Documentation

- Setup: [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md)
- Full guide: [README.md](README.md)
- Sheet structure: [SHEET_SETUP.md](SHEET_SETUP.md)

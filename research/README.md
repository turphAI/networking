# Company Research Files

This folder contains individual markdown files for researching companies.

## Folder Structure

```
research/
├── fintech/          # Fintech company research
├── healthcare/       # Healthcare company research
├── TEMPLATE.md       # Template for new research files
└── README.md         # This file
```

## Creating Research Files

### Option 1: Create from Google Sheet data

Automatically pull company data from your Google Sheets:

```bash
python create_company_research.py "Circle" --from-sheet --tracker fintech --region new-england
```

This will:
- Fetch company data from the Google Sheet
- Pre-fill the markdown file with existing data
- Save to `research/fintech/circle.md`

### Option 2: Create blank research file

Create an empty research file to fill out manually:

```bash
python create_company_research.py "New Company" --tracker fintech
```

## Listing Research Files

View all your research files:

```bash
# List all research files
python list_research.py

# Filter by tracker
python list_research.py --tracker fintech

# Search for specific content
python list_research.py --search "series b"

# Filter by status
python list_research.py --status "reached out"
```

## Opening Research Files

On Mac:
```bash
# Open in default editor
open research/fintech/circle.md

# Open in VS Code
code research/fintech/circle.md
```

## Research File Structure

Each research file includes:

- **Overview**: Company basics (industry, location, size, funding)
- **About**: Company description and mission
- **Key Products/Services**: What they build
- **Technology Stack**: Technologies they use
- **Design & UX Opportunities**: Where you can add value
- **Contacts**: People you're connecting with
- **Outreach Strategy**: Your approach and talking points
- **Meeting Notes**: Timestamped notes from conversations
- **Status Tracking**: Current status and next steps

## Workflow

### 1. Import companies to Google Sheets

```bash
python discover_and_import.py --industry fintech --region boston \
  --filter size=medium --filter min_funding=series-b
```

### 2. Create research files for interesting companies

```bash
python create_company_research.py "Circle" --from-sheet --tracker fintech --region new-england
```

### 3. Fill out the research file

Open the markdown file and add:
- Company research notes
- UX opportunities you've identified
- Contact information
- Outreach strategy

### 4. Track your outreach

Update the markdown file with:
- Meeting notes
- Follow-up actions
- Status changes

### 5. Update Google Sheet

When you make progress, update the Google Sheet:

```bash
python update_contact.py "Contact Name" "Circle" --status "Reached Out"
```

## Tips

- **Use headers to organize**: The markdown files use headers (##, ###) to organize sections
- **Add links**: Include links to LinkedIn profiles, portfolios, articles
- **Track dates**: Always note when you reached out or had meetings
- **Be specific**: Write detailed notes about opportunities and talking points
- **Stay updated**: Review and update your research files regularly

## Integration with Google Sheets

The research files complement your Google Sheets:

- **Google Sheets**: Quick overview, filtering, tracking many companies
- **Markdown Files**: Deep research, notes, strategy for specific companies

Use Google Sheets for the broad view, and markdown files for detailed research on companies you're actively pursuing.

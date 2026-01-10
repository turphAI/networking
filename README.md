# Networking Tracker Automation 🚀

A simple Python tool to manage your UX design networking outreach via Google Sheets. Perfect for designers learning to code!

## What This Does

This tool helps you:
- ✅ Add companies to your networking trackers (Fintech & HealthTech)
- ✅ Research and find design team contacts
- ✅ Update contact information and outreach status
- ✅ Track your networking progress in Google Sheets

## Your Trackers

- **Fintech Tracker**: [Open Sheet](https://docs.google.com/spreadsheets/d/1Ir2nA37z9iNxVCKHbhSSNK_VJsI49f6N/edit?gid=1176481834#gid=1176481834)
- **HealthTech Tracker**: [Open Sheet](https://docs.google.com/spreadsheets/d/1Y4djqEJoGqLuxLaMlDpa5DKjkWl3Zhf9/edit?gid=1664660466#gid=1664660466)

## Setup Instructions

### Step 1: Install Python

Make sure you have Python 3.8 or newer installed:

```bash
python3 --version
```

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Google Sheets API

This is the most important part! Follow these steps carefully:

#### 3.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" at the top
3. Click "New Project"
4. Name it "Networking Tracker" and click "Create"

#### 3.2 Enable Google Sheets API

1. In your new project, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on it and click "Enable"

#### 3.3 Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the consent screen:
   - User Type: External
   - App name: "Networking Tracker"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue" through the rest
4. Back to creating OAuth client ID:
   - Application type: "Desktop app"
   - Name: "Networking Tracker Desktop"
   - Click "Create"
5. Click "Download JSON"
6. Rename the downloaded file to `credentials.json`
7. Move it to this project folder (same folder as this README)

#### 3.4 First Time Authentication

Run any script for the first time:

```bash
python add_company.py "Test Company" --tracker fintech
```

A browser window will open asking you to:
1. Log in to your Google account
2. Grant permissions to access your spreadsheets
3. After approval, the script will save your credentials

The script will create a `token.json` file that saves your login for future use.

### Step 4: Configure Your Sheets (Optional)

The sheet IDs are already configured with defaults. If you want to customize settings, you have two options:

#### Option A: Use .env file (Recommended)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and update the sheet tab names if needed:
   ```
   FINTECH_SHEET_NAME=Sheet1
   HEALTHTECH_SHEET_NAME=Sheet1
   ```

The `.env` file is already in `.gitignore` so your customizations stay private.

#### Option B: Edit config.py directly

Open `config.py` and the defaults will be used if no `.env` file exists.

To find your sheet tab name, open your Google Sheet and look at the tab name at the bottom.

## How to Use

### Add a New Company

Add a company to research:

```bash
python add_company.py "Stripe" --tracker fintech
python add_company.py "Oscar Health" --tracker healthtech
```

What it does:
- Adds the company to your Google Sheet
- Creates a LinkedIn search URL for finding contacts
- Sets status to "To Research"

### Find Design Contacts

Get help researching a specific company:

```bash
python find_contacts.py "Stripe" --tracker fintech
```

This gives you:
- LinkedIn search URLs to find UX/Product designers
- Potential team pages to check on their website
- Step-by-step instructions for manual research

See all companies that need research:

```bash
python find_contacts.py --all --tracker fintech
```

### Update Company Info

Add contact information:

```bash
python update_status.py "Stripe" --tracker fintech \
  --contact "Jane Doe" \
  --title "Senior UX Designer" \
  --email "jane@stripe.com"
```

Update outreach status:

```bash
python update_status.py "Stripe" --tracker fintech --status "Reached Out"
```

Add notes:

```bash
python update_status.py "Stripe" --tracker fintech \
  --notes "Met at UX conference, follow up next week"
```

View current information:

```bash
python update_status.py "Stripe" --tracker fintech --show
```

Available status options:
- `To Research` - Need to find contacts
- `Researched` - Found contacts, ready to reach out
- `Reached Out` - Sent initial message
- `Responded` - They replied!
- `Meeting Scheduled` - Have a meeting set up
- `Follow Up` - Need to follow up
- `Not Interested` - Not a good fit

## Example Workflow

Here's a typical workflow:

```bash
# 1. Add companies you want to research
python add_company.py "Stripe" --tracker fintech
python add_company.py "Square" --tracker fintech
python add_company.py "Oscar Health" --tracker healthtech

# 2. Research the first company
python find_contacts.py "Stripe" --tracker fintech
# This shows you LinkedIn search URLs and potential team pages

# 3. After manually finding contacts on LinkedIn, add them:
python update_status.py "Stripe" --tracker fintech \
  --contact "Jane Doe" \
  --title "Senior UX Designer" \
  --email "jane@stripe.com" \
  --status "Researched"

# 4. After reaching out:
python update_status.py "Stripe" --tracker fintech \
  --status "Reached Out" \
  --notes "Sent InMail on 1/10"

# 5. After they respond:
python update_status.py "Stripe" --tracker fintech \
  --status "Responded" \
  --notes "Positive response, scheduling coffee chat"
```

## Understanding the Code

### File Structure

```
networking/
├── config.py                 # Your Google Sheet IDs and settings
├── sheets_manager.py         # Handles Google Sheets authentication & operations
├── company_researcher.py     # Helps find company info and contacts
├── add_company.py           # Script to add new companies
├── find_contacts.py         # Script to research contacts
├── update_status.py         # Script to update information
├── requirements.txt         # Python packages needed
├── .gitignore              # Files to exclude from git
└── README.md               # This file!
```

### How It Works

**sheets_manager.py**: This is the core module that talks to Google Sheets
- `_authenticate()`: Handles logging in to Google
- `read_sheet()`: Reads data from a sheet
- `write_sheet()`: Writes data to a sheet
- `append_row()`: Adds a new row to the end
- `find_row_by_value()`: Searches for a specific company
- `update_cell()`: Updates a single cell

**company_researcher.py**: Helps with research
- `create_company_research_template()`: Creates starter data for new companies
- `extract_contacts_from_linkedin()`: Generates LinkedIn search URLs
- `find_design_team_page()`: Suggests potential team pages to check

**Scripts** (add_company.py, find_contacts.py, update_status.py):
- These are the commands you run
- They use the managers to do the actual work
- They handle command-line arguments and user interaction

## Troubleshooting

### "credentials.json not found"

Make sure you've downloaded your credentials from Google Cloud Console and placed them in the project folder.

### "Permission denied" or "403 error"

Make sure you've:
1. Enabled the Google Sheets API in your Google Cloud project
2. Granted permissions when the browser opened
3. Are using the same Google account that owns the spreadsheets

### "Company not found"

Make sure:
1. The company name matches exactly (case-sensitive)
2. You're using the correct tracker (fintech vs healthtech)
3. The company has been added with `add_company.py` first

### Script shows wrong sheet name

Open `config.py` and update the sheet names to match your actual Google Sheet tab names.

## Privacy & Security

### Files That NEVER Go in GitHub (Already in .gitignore)

- **`credentials.json`** - OAuth credentials from Google Cloud. Download this yourself, keep it LOCAL only.
- **`token.json`** - Auto-generated authentication token. Stays LOCAL only.
- **`.env`** - Your personal configuration overrides. Stays LOCAL only.

These files are already in `.gitignore` so Git will refuse to commit them. If GitHub is blocking an upload mentioning secrets, that's **protecting you** - you shouldn't upload those files anyway!

### Files That ARE Safe to Commit

- ✅ All Python scripts (`.py` files)
- ✅ Documentation (`.md` files)
- ✅ `config.py` - Contains only default Sheet IDs (already public in your URLs)
- ✅ `.env.example` - Template with no actual secrets
- ✅ `requirements.txt` - List of packages

### What Each User Needs

When someone clones this repo, they need to:
1. Get their own `credentials.json` from Google Cloud Console
2. Place it in the project folder (never commit it!)
3. Run scripts - this creates their own `token.json`
4. Optionally create their own `.env` file with their sheet IDs

### If Credentials Get Compromised

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Credentials"
3. Delete the compromised OAuth client ID
4. Create a new one and download new `credentials.json`

## Next Steps

Want to extend this tool? Here are some ideas:

1. **Add email tracking**: Track when you sent emails and follow-ups
2. **Analytics**: Create a script to show success metrics
3. **Automated reminders**: Get notified when to follow up
4. **LinkedIn integration**: If you get LinkedIn API access, automate contact finding
5. **Email templates**: Generate personalized outreach emails
6. **Batch operations**: Add multiple companies from a CSV file

## Questions?

Common questions for beginners:

**Q: Do I need to keep the terminal open?**
A: No! Once a script finishes running, you can close it. The data is saved in Google Sheets.

**Q: Can I edit the sheets manually?**
A: Yes! You can edit directly in Google Sheets. The scripts just make it faster.

**Q: What if I mess something up?**
A: Google Sheets has version history (File > Version history). You can always undo changes.

**Q: Can someone else use this tool?**
A: Yes, but they need their own `credentials.json` and access to the Google Sheets.

## Learning Resources

Want to understand the code better?

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Command Line Basics](https://www.learnenough.com/command-line-tutorial)

Happy networking! 🎉

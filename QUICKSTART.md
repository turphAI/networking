# Quick Start Guide 🚀

New to coding? Start here!

## Setup (Do this once)

### 1. Open Terminal/Command Prompt

**Mac**: Press `Cmd + Space`, type "Terminal", press Enter
**Windows**: Press `Win + R`, type "cmd", press Enter
**Linux**: Press `Ctrl + Alt + T`

### 2. Navigate to this folder

```bash
cd /path/to/networking
```

(Replace `/path/to/networking` with where you saved this project)

### 3. Install Python packages

```bash
pip install -r requirements.txt
```

Wait for it to finish (might take a minute).

### 4. Get Google Sheets credentials

1. Go to https://console.cloud.google.com/
2. Create new project: "Networking Tracker"
3. Enable "Google Sheets API"
4. Create OAuth credentials (Desktop app)
5. Download as `credentials.json`
6. Put it in this folder

**Need detailed steps?** See [README.md](README.md#step-3-set-up-google-sheets-api)

### 5. Update config.py

Open `config.py` in a text editor and check:
- Sheet IDs are correct ✓
- Sheet names match your tabs (probably "Sheet1")

## Daily Use

### Add a company

```bash
python add_company.py "Company Name" --tracker fintech
```

Example:
```bash
python add_company.py "Stripe" --tracker fintech
```

### Research contacts

```bash
python find_contacts.py "Company Name" --tracker fintech
```

This gives you LinkedIn URLs to search manually.

### After finding contacts

```bash
python update_status.py "Company Name" --tracker fintech \
  --contact "Jane Doe" \
  --title "UX Designer" \
  --status "Researched"
```

### After reaching out

```bash
python update_status.py "Company Name" --tracker fintech \
  --status "Reached Out"
```

## Cheat Sheet

| What you want to do | Command |
|---------------------|---------|
| Add new company | `python add_company.py "NAME" --tracker TYPE` |
| Research company | `python find_contacts.py "NAME" --tracker TYPE` |
| See all needing research | `python find_contacts.py --all --tracker TYPE` |
| Add contact info | `python update_status.py "NAME" --tracker TYPE --contact "..." --title "..."` |
| Update status | `python update_status.py "NAME" --tracker TYPE --status "..."` |
| View company info | `python update_status.py "NAME" --tracker TYPE --show` |

**Replace:**
- `NAME` = Company name (e.g., "Stripe")
- `TYPE` = Either `fintech` or `healthtech`

## Status Options

- `To Research` → Need to find contacts
- `Researched` → Found contacts
- `Reached Out` → Sent message
- `Responded` → They replied!
- `Meeting Scheduled` → Meeting set up
- `Follow Up` → Need to follow up
- `Not Interested` → Not pursuing

## Common Errors

**"credentials.json not found"**
→ Download it from Google Cloud Console

**"Company not found"**
→ Check spelling, use exact name from sheet

**"Permission denied"**
→ Re-run and grant permissions in browser

## Tips

- Copy-paste company names from your sheet to avoid typos
- Use quotes around names: `"Company Name"` not `Company Name`
- Check your Google Sheet after each command to see changes
- Tab completion works! Type `python add_` then press Tab

## Example Session

```bash
# Add 3 companies
python add_company.py "Stripe" --tracker fintech
python add_company.py "Square" --tracker fintech
python add_company.py "Plaid" --tracker fintech

# Research first one
python find_contacts.py "Stripe" --tracker fintech
# (Go to LinkedIn, find Jane Doe - Senior UX Designer)

# Add contact
python update_status.py "Stripe" --tracker fintech \
  --contact "Jane Doe" \
  --title "Senior UX Designer" \
  --status "Researched"

# Reach out via LinkedIn/email, then:
python update_status.py "Stripe" --tracker fintech \
  --status "Reached Out" \
  --notes "Sent LinkedIn message on 1/10"
```

Need more help? Check the full [README.md](README.md)

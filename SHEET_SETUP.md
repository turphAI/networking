# Google Sheet Setup Guide

## Your Current Structure

Both your Fintech and HealthTech sheets have these 4 tabs:

### 1. Contacts Tab
**Purpose**: Track individual design contacts for networking

| Column | Header | What it's for |
|--------|--------|---------------|
| A | Company | Where they work |
| B | Name | Contact's full name |
| C | Role/Title | Their job title |
| D | LinkedIn Profile | Their personal LinkedIn URL |
| E | Background Notes | Info about them |
| F | Contact Status | Networking status |
| G | Last Outreach | Date you last contacted them |
| H | Notes | Additional notes |

**Used by**: `add_contact.py`, `update_contact.py`

### 2. New England Tab
**Purpose**: Track companies in New England region

| Column | Header | What it's for |
|--------|--------|---------------|
| A | Company | Company name |
| B | Location | City, State |
| C | Focus Area | What they do |
| D | AI/Innovation | AI-related info |
| E | Website/LinkedIn | Company website or LinkedIn |
| F | Contact Name | Person at company |
| G | Contact Role | Their role |
| H | Contact Info | Email/phone |
| I | Outreach Status | Research status |
| J | Next Steps | What to do next |
| K | Notes | Additional notes |

**Used by**: `add_company.py --region new-england`, `find_contacts.py --region new-england`

### 3. NYC Tab
**Purpose**: Track companies in NYC region

Same structure as New England tab (columns A-K)

**Used by**: `add_company.py --region nyc`, `find_contacts.py --region nyc`

### 4. Organization Tab
**Purpose**: Track organizations and networking events

| Column | Header | What it's for |
|--------|--------|---------------|
| A | Organization/Event | Name of org or event |
| B | Location | Where it's located |
| C | Type | Professional Org, Conference, Meetup, etc. |
| D | Description | What it's about |
| E | Timing/Frequency | When it happens |
| F | Contact/Website | How to reach them |
| G | Notes | Additional notes |

**Used by**: `add_organization.py`

## Important Notes

1. **Don't change tab names** - Scripts expect these exact names:
   - "Contacts"
   - "New England"
   - "NYC"
   - "Organization"

2. **Don't delete headers** - Row 1 must have column headers

3. **Don't rearrange columns** - Scripts expect columns in this exact order

4. **You can add more columns** - Just add them after the last column (to the right)
   ```python
   FINTECH_SHEET_NAME = "Your Tab Name Here"
   ```
3. **Sheet ID** - Already configured in `config.py` from your URLs
4. **Permissions** - Make sure your Google account has edit access to both sheets

## Example Sheet

Here's what your sheet might look like with some data:

| Company Name | Website | LinkedIn | Contact Name | Contact Title | Contact Email | Status | Notes |
|--------------|---------|----------|--------------|---------------|---------------|--------|-------|
| Stripe | https://stripe.com | https://linkedin.com/company/stripe | Jane Doe | Senior UX Designer | jane@stripe.com | Responded | Very interested! |
| Square | https://squareup.com | https://linkedin.com/company/square | John Smith | Design Lead | john@squareup.com | Reached Out | Sent on 1/5 |
| Plaid | https://plaid.com | https://linkedin.com/company/plaid | | | | To Research | Found on Built In |

## Status Workflow

Suggested status progression:

```
To Research
    ↓
Researched (found contacts)
    ↓
Reached Out (sent message)
    ↓
Responded (they replied)
    ↓
Meeting Scheduled (set up call)
    ↓
Follow Up (need to reconnect)
```

Or:
```
To Research
    ↓
Researched
    ↓
Not Interested (decided not to pursue)
```

## Tips for Organization

1. **Use filters**: Google Sheets lets you filter by status
2. **Conditional formatting**: Highlight rows based on status
   - Green for "Responded" or "Meeting Scheduled"
   - Yellow for "Reached Out"
   - Red for "Follow Up"
3. **Freeze header row**: View → Freeze → 1 row
4. **Sort**: Sort by company name or status
5. **Add formulas**:
   - Days since last contact: `=TODAY()-L2`
   - Auto-fill dates: `=TODAY()` when adding new companies

## Sharing Settings

If you're collaborating with someone:

1. Click "Share" in top-right of Google Sheet
2. Add their email
3. Give them "Editor" access
4. They'll need their own `credentials.json` to use the scripts

## Backup

Google Sheets auto-saves, but you can also:
- File → Version history → See version history
- File → Download → CSV or Excel (for local backup)
- Set up automatic backups using Google Takeout

## Troubleshooting

**"Values not showing up"**
- Refresh your Google Sheet
- Check you're on the correct tab
- Verify the sheet name in `config.py` matches exactly

**"Data in wrong columns"**
- The scripts assume columns A-H as shown above
- If your columns are different, you'll need to modify the column mapping in each script

**"Can't edit sheet"**
- Make sure you're logged in with the right Google account
- Check sheet permissions
- Verify `credentials.json` is for the right account

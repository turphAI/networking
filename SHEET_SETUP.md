# Google Sheet Setup Guide

## Recommended Sheet Structure

Your Google Sheets should have these columns (you can add more as needed):

| Column | Header | Description | Example |
|--------|--------|-------------|---------|
| A | Company Name | Name of the company | "Stripe" |
| B | Website | Company website | "https://stripe.com" |
| C | LinkedIn | LinkedIn company page | "https://linkedin.com/company/stripe" |
| D | Contact Name | Design contact name | "Jane Doe" |
| E | Contact Title | Their job title | "Senior UX Designer" |
| F | Contact Email | Email address | "jane@stripe.com" |
| G | Status | Outreach status | "Reached Out" |
| H | Notes | Additional notes | "Met at conference" |

## Setting Up Your Sheets

### Option 1: Create from scratch

1. Open your Google Sheet
2. Add the headers in row 1 (see table above)
3. Format the header row (bold, background color, etc.)
4. That's it! The scripts will add rows below

### Option 2: Copy this template

Create a new sheet and copy-paste this structure:

```
Company Name	Website	LinkedIn	Contact Name	Contact Title	Contact Email	Status	Notes
```

## Additional Columns (Optional)

Feel free to add more columns for your needs:

- **Phone** (Column I): Contact phone number
- **LinkedIn Profile** (Column J): Individual's LinkedIn
- **Date Added** (Column K): When you added them
- **Last Contact** (Column L): Last time you reached out
- **Next Follow-up** (Column M): When to follow up
- **Priority** (Column N): High/Medium/Low
- **Referral** (Column O): Who referred you

## Important Notes

1. **Don't delete the header row** - The scripts expect headers in row 1
2. **Sheet tab name** - Note the name of your tab (shown at bottom of Google Sheets). Update this in `config.py`:
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

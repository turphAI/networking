# How to Get Your credentials.json File

This guide walks you through getting Google Sheets API credentials step-by-step.

## Overview

You need `credentials.json` to let your scripts access Google Sheets. This is a one-time setup that takes about 10 minutes.

## Step-by-Step Instructions

### Step 1: Go to Google Cloud Console

1. Open your browser and go to: https://console.cloud.google.com/
2. Sign in with your Google account (use the same account that has access to your Google Sheets)

### Step 2: Create a New Project

1. Click the project dropdown at the top (says "Select a project")
2. Click "NEW PROJECT" in the top right
3. Enter project name: `Networking Tracker`
4. Leave organization as is (usually "No organization")
5. Click "CREATE"
6. Wait a few seconds for it to create
7. Make sure your new project is selected in the dropdown

### Step 3: Enable Google Sheets API

1. In the left sidebar, click "APIs & Services" → "Library"
   - Or use the search bar at top and search "API Library"
2. In the API Library search box, type: `Google Sheets API`
3. Click on "Google Sheets API" from the results
4. Click the blue "ENABLE" button
5. Wait for it to enable (takes a few seconds)

### Step 4: Configure OAuth Consent Screen

Before creating credentials, you need to set up the consent screen:

1. In the left sidebar, click "APIs & Services" → "OAuth consent screen"
2. Choose "External" as User Type
3. Click "CREATE"
4. Fill in the required fields:
   - **App name**: `Networking Tracker`
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
5. Click "SAVE AND CONTINUE"
6. On "Scopes" page, just click "SAVE AND CONTINUE" (we don't need to add scopes here)
7. On "Test users" page, click "ADD USERS"
   - Enter your email address
   - Click "ADD"
   - Click "SAVE AND CONTINUE"
8. Click "BACK TO DASHBOARD"

### Step 5: Create OAuth Credentials

1. In the left sidebar, click "APIs & Services" → "Credentials"
2. Click "CREATE CREDENTIALS" at the top
3. Select "OAuth client ID"
4. For Application type, select "Desktop app"
5. Name: `Networking Tracker Desktop`
6. Click "CREATE"
7. A popup appears with your credentials - click "DOWNLOAD JSON"

### Step 6: Rename and Move the File

1. The downloaded file has a long name like `client_secret_123456789.json`
2. Rename it to exactly: `credentials.json`
3. Move it to your networking project folder (where this README is)

### Step 7: Verify Setup

Run the setup checker:

```bash
python setup_check.py
```

Should show:
```
✅ credentials.json found
```

## Security Notes

### What is credentials.json?

- It contains your OAuth client ID and secret
- It allows applications to request access to your Google account
- It does NOT contain your password or direct access to your data

### Keeping it Safe

- ✅ Keep it in your project folder
- ✅ It's in `.gitignore` so it won't be committed to git
- ❌ Never share it publicly
- ❌ Never commit it to GitHub
- ❌ Never email it or put it in Slack/Discord

### If You Lose It

Just create a new one:
1. Go back to Google Cloud Console → Credentials
2. Delete the old OAuth client ID
3. Create a new one following Step 5 above

### If It Gets Compromised

1. Go to Google Cloud Console
2. APIs & Services → Credentials
3. Find your OAuth client ID
4. Click the trash icon to delete it
5. Create a new one

## Troubleshooting

### "Access blocked: This app's request is invalid"

You need to complete the OAuth consent screen setup (Step 4).

### "The project does not have access to this API"

Make sure you enabled the Google Sheets API (Step 3) in the correct project.

### "Redirect URI mismatch"

Make sure you selected "Desktop app" not "Web application" when creating credentials.

### "Cannot find credentials.json"

Make sure:
- The file is named exactly `credentials.json` (not `credentials.json.json` or `Credentials.json`)
- It's in the same folder as your Python scripts
- You're running commands from the project folder

### "Invalid client secret"

The credentials.json file might be corrupted. Download it again from Google Cloud Console.

## What Happens Next?

After you have `credentials.json`:

1. First time you run a script, your browser opens
2. You'll see "Google hasn't verified this app" - click "Advanced" → "Go to Networking Tracker (unsafe)"
   - This is normal! It's YOUR app, you just haven't submitted it for Google's verification
3. Click "Allow" to grant permissions
4. A file called `token.json` is created
5. Future runs use `token.json` automatically - no more browser popups!

## Understanding the Files

- **credentials.json**: Your app's identity (like a username)
- **token.json**: Your access token (like being logged in)

Think of it like a website:
- credentials.json = your email address for login
- token.json = the "Stay logged in" cookie

## Advanced: Scopes

The scripts request these permissions:
- `https://www.googleapis.com/auth/spreadsheets` - Read and write to spreadsheets

This is defined in `config.py`. You can check what permissions were granted by looking at your [Google Account permissions](https://myaccount.google.com/permissions).

## Questions?

**Q: Do I need to do this for each computer?**
A: You need `credentials.json` on each computer, but you can copy `token.json` to avoid re-authenticating.

**Q: Can I share token.json with others?**
A: No, it's personal to your Google account.

**Q: How long does token.json last?**
A: Usually a long time, but it can expire. Just re-run a script to refresh it.

**Q: Can I use a different Google account?**
A: Yes, delete `token.json` and run a script again. It will prompt you to log in with a different account.

**Q: Is this safe?**
A: Yes, you're creating credentials for your own app. Google's OAuth is secure and you can revoke access anytime.

## Next Steps

Once you have `credentials.json`:

1. Run: `python setup_check.py` to verify everything
2. Run: `python add_company.py "Test Company" --tracker fintech` to test
3. Grant permissions in the browser
4. Check your Google Sheet to see if it worked!

See [QUICKSTART.md](QUICKSTART.md) for usage examples.

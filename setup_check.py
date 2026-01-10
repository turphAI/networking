#!/usr/bin/env python3
"""
Setup Checker
Verify your environment is set up correctly
"""

import os
import sys


def check_setup():
    """Check if everything is set up correctly"""
    print("\n🔍 Checking your setup...\n")

    all_good = True

    # Check Python version
    print("1️⃣  Python version:")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro}")
        print("   ⚠️  Python 3.8+ required")
        all_good = False

    # Check for credentials.json
    print("\n2️⃣  Google credentials:")
    if os.path.exists('credentials.json'):
        print("   ✅ credentials.json found")
    else:
        print("   ❌ credentials.json NOT found")
        print("   ⚠️  Download from Google Cloud Console")
        all_good = False

    # Check for config.py
    print("\n3️⃣  Configuration:")
    if os.path.exists('config.py'):
        print("   ✅ config.py found")
        try:
            import config
            print(f"   ✅ Fintech Sheet ID: {config.FINTECH_SHEET_ID[:20]}...")
            print(f"   ✅ HealthTech Sheet ID: {config.HEALTHTECH_SHEET_ID[:20]}...")
        except Exception as e:
            print(f"   ⚠️  Error reading config: {e}")
    else:
        print("   ❌ config.py NOT found")
        all_good = False

    # Check for required packages
    print("\n4️⃣  Required packages:")
    required_packages = [
        'google.auth',
        'google_auth_oauthlib',
        'googleapiclient',
        'requests',
        'bs4',
        'pandas'
    ]

    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} NOT installed")
            print("   ⚠️  Run: pip install -r requirements.txt")
            all_good = False

    # Check for scripts
    print("\n5️⃣  Scripts:")
    scripts = [
        'sheets_manager.py',
        'company_researcher.py',
        'add_company.py',
        'find_contacts.py',
        'update_status.py'
    ]

    for script in scripts:
        if os.path.exists(script):
            print(f"   ✅ {script}")
        else:
            print(f"   ❌ {script} NOT found")
            all_good = False

    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("✅ All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("1. Run: python add_company.py 'Test Company' --tracker fintech")
        print("2. This will prompt you to authenticate with Google")
        print("3. After that, you're all set!")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nSee README.md for detailed setup instructions.")

    print("=" * 50 + "\n")


if __name__ == "__main__":
    check_setup()

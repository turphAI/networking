#!/usr/bin/env python3
"""
Test what config values are being loaded
"""

import os
from dotenv import load_dotenv

print("🔍 Testing config loading...\n")

# Load .env file
print("1. Loading .env file...")
load_dotenv()

print("2. Reading environment variables:")
fintech_id = os.getenv('FINTECH_SHEET_ID', 'NOT_FOUND')
healthtech_id = os.getenv('HEALTHTECH_SHEET_ID', 'NOT_FOUND')

print(f"   FINTECH_SHEET_ID from env: {fintech_id}")
print(f"   HEALTHTECH_SHEET_ID from env: {healthtech_id}")

print("\n3. Reading from config.py:")
import config
print(f"   config.FINTECH_SHEET_ID: {config.FINTECH_SHEET_ID}")
print(f"   config.HEALTHTECH_SHEET_ID: {config.HEALTHTECH_SHEET_ID}")

print("\n4. Checking .env file directly:")
if os.path.exists('.env'):
    print("   ✅ .env file exists")
    with open('.env', 'r') as f:
        content = f.read()
        print("   Contents:")
        for line in content.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"     {line}")
else:
    print("   ❌ .env file not found!")

print("\n5. Current working directory:")
print(f"   {os.getcwd()}")

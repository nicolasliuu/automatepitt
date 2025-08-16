#!/usr/bin/env python3
"""
Setup script for Google Sheets API authentication
"""

import os
import json
from pathlib import Path

def check_credentials():
    """Check if credentials.json exists and is valid"""
    creds_file = Path('credentials.json')
    
    if not creds_file.exists():
        print("❌ credentials.json not found!")
        print("\nTo set up Google API access:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Sheets API and Google Drive API")
        print("4. Go to 'APIs & Services' > 'Credentials'")
        print("5. Click 'Create Credentials' > 'Service Account'")
        print("6. Fill in service account details")
        print("7. Click 'Create and Continue' then 'Done'")
        print("8. Click on your service account")
        print("9. Go to 'Keys' tab > 'Add Key' > 'Create new key' > 'JSON'")
        print("10. Download and rename to 'credentials.json'")
        print("11. Place it in this directory")
        return False
    
    try:
        with open(creds_file, 'r') as f:
            creds_data = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in creds_data]
        
        if missing_fields:
            print(f"❌ credentials.json is missing required fields: {missing_fields}")
            return False
        
        print("✅ credentials.json found and appears valid")
        print(f"   Project ID: {creds_data.get('project_id', 'N/A')}")
        print(f"   Client Email: {creds_data.get('client_email', 'N/A')}")
        return True
        
    except json.JSONDecodeError:
        print("❌ credentials.json is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials.json: {e}")
        return False

def test_google_connection():
    """Test the Google Sheets connection"""
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        
        print("\n🔗 Testing Google Sheets connection...")
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        print("✅ Successfully authenticated with Google!")
        
        # Try to open the spreadsheet
        try:
            sheet = client.open("2025 Internships")
            print("✅ Successfully opened '2025 Internships' spreadsheet!")
            print(f"   Sheet ID: {sheet.id}")
            print(f"   URL: {sheet.url}")
            return True
        except gspread.SpreadsheetNotFound:
            print("❌ Spreadsheet '2025 Internships' not found!")
            print("\nTo fix this:")
            print("1. Create a Google Sheet named '2025 Internships'")
            print("2. Share it with your service account email (found in credentials.json)")
            print("3. Give the service account 'Editor' permissions")
            return False
            
    except ImportError as e:
        print(f"❌ Missing required packages: {e}")
        print("Run: source venv/bin/activate && pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def main():
    print("🚀 Google Sheets API Setup Checker")
    print("=" * 40)
    
    creds_ok = check_credentials()
    
    if creds_ok:
        test_google_connection()
    
    print("\n" + "=" * 40)
    if creds_ok:
        print("🎉 Setup complete! You can now run: python script.py")
    else:
        print("⚠️  Please complete the setup steps above")

if __name__ == "__main__":
    main()

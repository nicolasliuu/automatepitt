import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Function to scrape GitHub page
def scrape_github_jobs(url, stop_at_job):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for item in soup.find_all('tr'):
        try:
            columns = item.find_all('td')
            if len(columns) < 4:
                print("Skipped")
                continue  # Skip rows that don't have enough columns
            role = columns[1].text.strip()
            link_tag = columns[3].find('a')
            if link_tag is None:
                continue  # Skip if there's no link
            link = link_tag['href']
            if (role, link) == stop_at_job:
                break
            jobs.append((role, link))
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    return jobs

# Function to find the most recent job in the spreadsheet
def get_most_recent_job(sheet):
    try:
        # Get all values at once to minimize API calls
        all_values = sheet.get_all_values()
        if len(all_values) <= 1:  # Only header or empty
            return None
        
        # Get the last row (most recent job)
        last_row = all_values[-1]
        if len(last_row) >= 2:
            return (last_row[0], last_row[1])  # role, link
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not get most recent job: {e}")
        return None

# Function to update Google Sheets
def update_google_sheets(sheet, jobs):
    if not jobs:
        return
    
    print(f"📊 Checking for duplicates and adding {len(jobs)} new jobs...")
    
    try:
        # Get all existing data ONCE to avoid multiple API calls
        existing_roles = sheet.col_values(1)
        existing_links = sheet.col_values(2)
        
        # Filter out duplicates
        new_jobs = []
        for role, link in jobs:
            if role not in existing_roles and link not in existing_links:
                new_jobs.append([role, link])
            else:
                print(f"⏭️  Skipped duplicate: {role}")
        
        if not new_jobs:
            print("✅ No new jobs to add!")
            return
        
        print(f"📝 Adding {len(new_jobs)} new jobs...")
        
        # Batch add all new jobs at once (much more efficient)
        sheet.append_rows(new_jobs)
        print(f"✅ Successfully added {len(new_jobs)} new jobs!")
        
        # Small delay to be respectful to Google's API
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error in batch update: {e}")
        # Fallback to individual adds if batch fails
        print("🔄 Falling back to individual job addition...")
        for role, link in jobs:
            try:
                sheet.append_row([role, link])
                print(f"✅ Added: {role}")
                time.sleep(1)  # Rate limiting
            except Exception as e2:
                print(f"❌ Error adding {role}: {e2}")
                time.sleep(2)

# Setup Google Sheets API
def setup_google_sheets(sheet_name="NG Recruiting"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

# Main function
def main():
    github_url = 'https://github.com/SimplifyJobs/New-Grad-Positions'
    sheet_name = "NG Recruiting"
    
    try:
        sheet = setup_google_sheets(sheet_name)
        print(f"✅ Connected to '{sheet_name}' spreadsheet")
        
        print("\n🔍 Scraping new jobs from GitHub...")
        most_recent_job = get_most_recent_job(sheet)
        jobs = scrape_github_jobs(github_url, most_recent_job)
        
        if jobs:
            print(f"Found {len(jobs)} new jobs!")
            update_google_sheets(sheet, jobs)
            print("\n✅ Done! New jobs added to your spreadsheet.")
        else:
            print("No new jobs found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your Google Sheet exists and is shared with your service account.")

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    last_row = len(sheet.col_values(1))  # Get the number of rows in the first column
    if last_row == 0:
        return None  # No jobs in the sheet yet
    most_recent_role = sheet.cell(last_row, 1).value
    most_recent_link = sheet.cell(last_row, 2).value
    return (most_recent_role, most_recent_link)

# Function to update Google Sheets
def update_google_sheets(sheet, jobs):
    for role, link in jobs:
        sheet.append_row([role, link])

# Setup Google Sheets API
def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("2025 Internships").sheet1
    return sheet

# Main function
def main():
    github_url = 'https://github.com/SimplifyJobs/Summer2025-Internships'
    sheet = setup_google_sheets()
    most_recent_job = get_most_recent_job(sheet)
    jobs = scrape_github_jobs(github_url, most_recent_job)
    update_google_sheets(sheet, jobs)

if __name__ == "__main__":
    main()

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets API
def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def list_spreadsheets():
    client = setup_google_sheets()
    sheets = client.openall()
    for sheet in sheets:
        print(sheet.title)

def main():
    list_spreadsheets()

if __name__ == "__main__":
    main()
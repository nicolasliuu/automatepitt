# AutomatePitt - GitHub Jobs to Google Sheets

This script automatically scrapes internship opportunities from the [Summer 2025 Internships](https://github.com/SimplifyJobs/Summer2025-Internships) GitHub repository and updates a Google Sheet with new job listings.

## Features

- Scrapes GitHub job listings automatically
- Tracks the most recent job to avoid duplicates
- Updates Google Sheets in real-time
- Handles errors gracefully

## Prerequisites

- Python 3.7+
- Google Cloud Platform account
- Google Sheets API enabled
- Google Drive API enabled

## Setup Instructions

### 1. Clone and Setup Environment

```bash
# Navigate to your project directory
cd automatepitt

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Cloud Platform Setup

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** or select an existing one
3. **Enable APIs:**
   - Go to "APIs & Services" > "Library"
   - Search for and enable "Google Sheets API"
   - Search for and enable "Google Drive API"

### 3. Create Service Account

1. **Go to "APIs & Services" > "Credentials"**
2. **Click "Create Credentials" > "Service Account"**
3. **Fill in service account details:**
   - Name: `automatepitt-sheets` (or any name you prefer)
   - Description: `Service account for automating Google Sheets updates`
4. **Click "Create and Continue"**
5. **Skip optional steps and click "Done"**
6. **Click on your newly created service account**
7. **Go to "Keys" tab**
8. **Click "Add Key" > "Create new key" > "JSON"**
9. **Download the JSON file**
10. **Rename it to `credentials.json`**
11. **Place it in your project directory** (same folder as `script.py`)

### 4. Create and Share Google Sheet

1. **Create a new Google Sheet** named "2025 Internships"
2. **Add headers** in the first row:
   - Column A: "Role"
   - Column B: "Link"
3. **Share the sheet:**
   - Click "Share" in the top right
   - Add your service account email (found in `credentials.json` under `client_email`)
   - Give it "Editor" permissions
   - Make sure the sheet is accessible to the service account

### 5. Test Setup

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Run the setup checker
python setup_google_api.py
```

This will verify your credentials and test the connection to Google Sheets.

### 6. Run the Script

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Run the main script
python script.py
```

## File Structure

```
automatepitt/
├── script.py              # Main automation script
├── setup_google_api.py    # Setup verification script
├── requirements.txt       # Python dependencies
├── credentials.json      # Google API credentials (you need to add this)
├── venv/                 # Virtual environment
└── README.md            # This file
```

## How It Works

1. **Scraping**: The script scrapes the GitHub repository for internship listings
2. **Tracking**: It remembers the most recent job to avoid duplicates
3. **Updating**: New jobs are automatically added to your Google Sheet
4. **Error Handling**: The script continues running even if individual jobs fail to process

## Troubleshooting

### Common Issues

1. **"credentials.json not found"**
   - Make sure you downloaded the service account key and renamed it to `credentials.json`
   - Place it in the same directory as `script.py`

2. **"Spreadsheet not found"**
   - Create a Google Sheet named exactly "2025 Internships"
   - Share it with your service account email
   - Give the service account Editor permissions

3. **Authentication errors**
   - Verify your Google Cloud project has the required APIs enabled
   - Check that your service account has the correct permissions
   - Ensure your `credentials.json` file is valid and complete

4. **Import errors**
   - Make sure you're in your virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

### Getting Help

- Check the setup script output for specific error messages
- Verify your Google Cloud Console settings
- Ensure your Google Sheet permissions are correct

## Security Notes

- **Never commit `credentials.json` to version control**
- **Keep your service account keys secure**
- **Only grant the minimum necessary permissions**
- **Consider using environment variables for production deployments**

## License

This project is for educational and personal use. Please respect the terms of service for both GitHub and Google Sheets APIs.

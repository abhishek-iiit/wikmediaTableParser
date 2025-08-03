import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_SHEETS_API_URL = os.getenv('GOOGLE_SHEETS_API_URL')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE = os.getenv('RANGE')
VALUE_INPUT_OPTION = os.getenv('VALUE_INPUT_OPTION', 'RAW')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


def build_api_endpoint():
    if not (GOOGLE_SHEETS_API_URL and SPREADSHEET_ID and RANGE):
        raise Exception('Missing Google Sheets API configuration in .env')
    return f"{GOOGLE_SHEETS_API_URL}/{SPREADSHEET_ID}/values/{RANGE}:append"


def append_to_google_sheets(data):
    url = build_api_endpoint()
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    body = {
        'values': data
    }
    params = {
        'valueInputOption': VALUE_INPUT_OPTION
    }
    response = requests.post(url, headers=headers, params=params, json=body)
    if response.status_code == 401:
        raise Exception('Unauthorized: ACCESS_TOKEN may have expired.')
    if response.status_code == 404:
        raise Exception('Not Found: Check SPREADSHEET_ID and permissions.')
    if not response.ok:
        raise Exception(f'Error appending to Google Sheets: {response.text}')
    return response.json()

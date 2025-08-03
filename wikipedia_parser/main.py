import os
from dotenv import load_dotenv
from wikipedia_parser.steps import (
    open_page, parse_number, loop_step, extract_html, call_api, detour,
    fill_text_field, click, check_box
)
from bs4 import BeautifulSoup
import re

load_dotenv()

PAGE_URL = os.getenv('PAGE_URL')
TABLE_SELECTOR = os.getenv('TABLE_SELECTOR')
ROW_COUNT = os.getenv('ROW_COUNT', '10')
GOOGLE_SHEETS_API_URL = os.getenv('GOOGLE_SHEETS_API_URL')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE = os.getenv('RANGE')
VALUE_INPUT_OPTION = os.getenv('VALUE_INPUT_OPTION', 'RAW')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


def clean_cell(text):
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def main():
    # Step 1: Open page
    html = open_page(PAGE_URL)

    # Step 2: Parse number of rows
    n_rows = parse_number(ROW_COUNT)

    # Step 3: Extract table rows
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one(TABLE_SELECTOR)
    if not table:
        raise Exception(f"Table not found for selector: {TABLE_SELECTOR}")
    rows = table.find_all('tr')[1:n_rows+1]  # skip header, get first n_rows

    extracted_data = []
    header = ["Year", "Winner", "Score", "Runners-up"]

    def extract_row(row, idx):
        cols = row.find_all(['td', 'th'])
        if len(cols) < 4:
            return
        year = clean_cell(cols[0].get_text())
        winner = clean_cell(cols[1].get_text())
        score = clean_cell(cols[2].get_text()).replace('-', '–')
        runners_up = clean_cell(cols[3].get_text())
        extracted_data.append([year, winner, score, runners_up])

    # Step 4: Loop over rows and extract data
    loop_step(rows, extract_row)
    # Prepend header
    extracted_data.insert(0, header)

    # Step 5: Detour (if no data, abort)
    def abort():
        print("No data extracted. Aborting.")
        exit(1)
    detour(len(extracted_data) == 0, abort)

    # Step 6: Call API (Google Sheets)
    url = f"{GOOGLE_SHEETS_API_URL}/{SPREADSHEET_ID}/values/{RANGE}:append"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    params = {
        'valueInputOption': VALUE_INPUT_OPTION
    }
    body = {
        'values': extracted_data
    }
    response = call_api(url, headers, params, body)
    if response.status_code == 200:
        print("Data successfully appended to Google Sheets.")
    elif response.status_code == 401:
        print("Unauthorized: ACCESS_TOKEN may have expired.")
    elif response.status_code == 404:
        print("Not Found: Check SPREADSHEET_ID and permissions.")
    else:
        print(f"Error appending to Google Sheets: {response.text}")

if __name__ == '__main__':
    main()

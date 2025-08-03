import os
import requests
from dotenv import load_dotenv
from wikipedia_parser.extractor import extract_table_data
from wikipedia_parser.sheets import append_to_google_sheets

load_dotenv()

PAGE_URL = os.getenv('PAGE_URL')
TABLE_SELECTOR = os.getenv('TABLE_SELECTOR')
ROW_COUNT = int(os.getenv('ROW_COUNT', 10))


def main():
    try:
        print(f"Fetching Wikipedia page: {PAGE_URL}")
        resp = requests.get(PAGE_URL)
        resp.raise_for_status()
        print("Extracting table data...")
        data = extract_table_data(resp.text, TABLE_SELECTOR, ROW_COUNT)
        print(f"Extracted {len(data)} rows. Appending to Google Sheets...")
        result = append_to_google_sheets(data)
        print("Data successfully appended to Google Sheets.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()

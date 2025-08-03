import re
from bs4 import BeautifulSoup

def clean_cell(cell):
    text = re.sub(r'\[.*?\]', '', cell.get_text(separator=' ', strip=True))
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_table_data(html, selector, row_count):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one(selector)
    if not table:
        raise ValueError(f"Table not found with selector: {selector}")
    rows = table.find_all('tr')[1:]  # skip header
    data = []
    for row in rows[:row_count]:
        cols = row.find_all(['td', 'th'])
        if len(cols) < 4:
            continue
        year = clean_cell(cols[0])
        winner = clean_cell(cols[1])
        score = clean_cell(cols[2])
        runners_up = clean_cell(cols[3])
        score = score.replace('-', '–')
        data.append([year, winner, score, runners_up])
    return data

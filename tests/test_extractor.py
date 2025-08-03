import pytest
from wikipedia_parser.extractor import extract_table_data

# Example HTML for testing
def test_extract_table_data():
    html = '''<table><tr><th>Year</th><th>Winner</th><th>Score</th><th>Runners-up</th></tr>
    <tr><td>1930</td><td>Uruguay</td><td>4–2</td><td>Argentina</td></tr>
    <tr><td>1934</td><td>Italy</td><td>2–1</td><td>Czechoslovakia</td></tr></table>'''
    selector = 'table'
    data = extract_table_data(html, selector, 2)
    assert data == [
        ['1930', 'Uruguay', '4–2', 'Argentina'],
        ['1934', 'Italy', '2–1', 'Czechoslovakia']
    ]

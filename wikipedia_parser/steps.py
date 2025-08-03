import requests
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

# --- Step Library Implementations ---

def open_page(url):
    """Open page: Navigates to a specified URL and returns HTML content."""
    resp = requests.get(url)
    resp.raise_for_status()
    logger.info("Step finished: open_page")
    return resp.text

def parse_number(str_val):
    """Parse number: Converts a string to int."""
    result = int(str_val)
    logger.info("Step finished: parse_number")
    return result

def loop_step(iterable, func):
    """Loop: Execute a function for each item in iterable (index starts at 1)."""
    for idx, item in enumerate(iterable, 1):
        try:
            func(item, idx)
        except Exception as e:
            logger.error(f"Loop error at index {idx}: {e}")
            continue
    logger.info("Step finished: loop_step")

def extract_html(dom_path, html, row_idx=None):
    """ExtractHTML: Extracts text from a DOM path (CSS selector). Optionally for a specific row."""
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.select_one(dom_path) if row_idx is None else soup.select(dom_path)[row_idx]
    if not element:
        raise ValueError(f"Element not found for selector: {dom_path}")
    logger.info("Step finished: extract_html")
    return element.get_text(separator=' ', strip=True)

def call_api(url, headers, params, body):
    """Call API: Makes a POST request (like Postman)."""
    response = requests.post(url, headers=headers, params=params, json=body)
    logger.info("Step finished: call_api")
    return response

def detour(condition, true_func, false_func=None):
    """Detour: Conditional execution (if/else)."""
    if condition:
        result = true_func()
        logger.info("Step finished: detour (true branch)")
        return result
    elif false_func:
        result = false_func()
        logger.info("Step finished: detour (false branch)")
        return result
    logger.info("Step finished: detour (no branch)")
    return None

def fill_text_field(dom_path, value, html):
    """Fill text field: Stub for RPA step (not used in this workflow)."""
    logger.info(f"Step finished: fill_text_field for {dom_path}")
    return html

def click(dom_path, html):
    """Click: Stub for RPA step (not used in this workflow)."""
    logger.info(f"Step finished: click for {dom_path}")
    return html

def check_box(dom_path, value, html):
    """Check Box: Stub for RPA step (not used in this workflow)."""
    logger.info(f"Step finished: check_box for {dom_path}")
    return html

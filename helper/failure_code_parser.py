from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging

# Assuming logger is configured elsewhere in your project
logger = logging.getLogger(__name__)


class FailureCodeParser:
    """
    Parser dedicated to extracting the 'Failure Codes' table from HTML content.
    Adheres to the Single Responsibility Principle by isolating parsing logic.
    """

    def __init__(self,
                 html_content: str):
        """
        Initializes the parser with raw HTML string.
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def parse(self) -> List[Dict[str, str]]:
        """
        Main orchestration method to extract table data.
        Returns a list of dictionaries mapping column headers to row values.
        """
        table = self.soup.find('table', attrs={'aria-label': 'Failure Codes'})

        if not table:
            logger.warning("Table with aria-label='Failure Codes' not found in the provided HTML.")
            return []

        headers = self._extract_headers(table)
        if not headers:
            logger.warning("Could not extract headers from the Failure Codes table.")
            return []

        return self._extract_rows(table, headers)

    def _extract_headers(self,
                         table) -> List[str]:
        """
        Helper method to cleanly extract table headers.
        Handles tables with or without a proper <thead> tag.
        """
        header_row = table.find('thead')
        if not header_row:
            # Fallback: Treat the very first <tr> as the header row
            header_row = table.find('tr')

        if not header_row:
            return []

        # List comprehension is highly Pythonic here for clean transformation
        return [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

    def _extract_rows(self,
                      table,
                      headers: List[str]) -> List[Dict[str, str]]:
        """
        Helper method to extract table data rows and zip them with headers.
        """
        parsed_data = []

        # Prefer standard <tbody> tags, fallback to all <tr> tags (skipping the header)
        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]

        for row in rows:
            cells = row.find_all('td')

            # Defensive programming: Ensure the row matches header length
            if len(cells) == len(headers):
                # Dictionary comprehension securely maps header strings to cell values
                row_dict = {
                    headers[i]: cells[i].get_text(strip=True)
                    for i in range(len(headers))
                }
                parsed_data.append(row_dict)
            else:
                logger.debug(f"Skipping malformed row: expected {len(headers)} cells, found {len(cells)}.")

        return parsed_data
# src/connectors/quote_connector.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class QuoteConnector:
    def __init__(self, base_url="http://quotes.toscrape.com"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def _parse_page(self, html):
        """Extracts data from a single HTML page."""
        soup = BeautifulSoup(html, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        page_data = []

        for q in quotes:
            page_data.append({
                "text": q.find("span", class_="text").get_text(),
                "author": q.find("small", class_="author").get_text(),
                "tags": [tag.get_text() for tag in q.find_all("a", class_="tag")],
                "scraped_at": datetime.now().isoformat()
            })
        
        # Look for the 'Next' button
        next_btn = soup.find("li", class_="next")
        next_url = self.base_url + next_btn.find("a")["href"] if next_btn else None
        
        return page_data, next_url

    def fetch_all(self, max_pages=None):
        """Orchestrates the multi-page scraping process."""
        all_data = []
        current_url = self.base_url
        pages_scraped = 0

        while current_url:
            if max_pages and pages_scraped >= max_pages:
                break
                
            logger.info(f"Fetching: {current_url}")
            response = requests.get(current_url, headers=self.headers)
            response.raise_for_status()

            data, next_url = self._parse_page(response.text)
            all_data.extend(data)
            
            current_url = next_url
            pages_scraped += 1

        return pd.DataFrame(all_data)

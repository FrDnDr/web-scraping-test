# src/connectors/quote_connector.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class BookConnector:
    def __init__(self, base_url="https://books.toscrape.com/"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def _parse_page(self, html, current_url):
        """Extracts data from a single HTML page."""
        soup = BeautifulSoup(html, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        page_data = []

        for b in books:
            page_data.append({
                "title": b.h3.a["title"],
                "price": b.find("p", class_="price_color").get_text(),
                "rating": b.p["class"][1], # e.g., "Three"
                "availability": b.find("p", class_="instock availability").get_text().strip(),
                "scraped_at": datetime.now().isoformat()
            })
        
        # Look for the 'Next' button
        next_btn = soup.find("li", class_="next")
        
        # URLJOIN handles relative paths like "page-3.html" perfectly 
        next_url = urljoin(current_url, next_btn.find("a")["href"]) if next_btn else None

        return page_data, next_url

    def fetch_all(self, max_pages=None):
        all_data = []
        current_url = self.base_url
        pages_scraped = 0
        while current_url:
            if max_pages and pages_scraped >= max_pages:
                break
                
            logger.info(f"Fetching: {current_url}")
            response = requests.get(current_url, headers=self.headers)
            response.raise_for_status()
            # Pass the current URL to help with relative links
            data, next_url = self._parse_page(response.text, current_url)
            all_data.extend(data)
            
            current_url = next_url
            pages_scraped += 1
        return pd.DataFrame(all_data)

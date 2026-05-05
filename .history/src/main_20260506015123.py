# src/main.py
import os
import logging
from connectors.quote_connector import QuoteConnector

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    # Initialize connector
    scraper = QuoteConnector()
    
    # 1. Fetch Data
    print("🚀 Starting Quote Scraper...")
    df = scraper.fetch_all(max_pages=5) # Limit to 5 pages for testing
    
    # 2. Process / Save Data
    if not df.empty:
        os.makedirs("data", exist_ok=True)
        output_path = "data/quotes_modular.csv"
        df.to_csv(output_path, index=False)
        
        print(f"✅ Success! Scraped {len(df)} quotes.")
        print(f"📊 Data saved to: {output_path}")
    else:
        print("⚠️ No data found.")

if __name__ == "__main__":
    main()

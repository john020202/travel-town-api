import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# 1. Setup the path for our "Database" (a JSON file)
FILE_PATH = "api/links.json"

# Load existing links so we don't save duplicates
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
else:
    data = []

# Create a set of existing URLs for fast checking
existing_links = {item['url'] for item in data}

# 2. Scrape new links
# REPLACE THIS URL with the site you actually want to scrape
TARGET_URL = "https://example-travel-town-aggregator.com" 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(TARGET_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    new_entries = []
    
    # REPLACE this logic to target the specific HTML elements containing the reward links
    # For example, finding all <a> tags
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        # Check if it looks like a reward link AND we haven't saved it yet
        if "traveltown" in href and href not in existing_links: 
            new_entries.append({
                "url": href,
                "date_found": datetime.now().isoformat()
            })
            existing_links.add(href)

    # 3. Save the updated data back to the JSON file
    if new_entries:
        data.extend(new_entries)
        
        # Ensure the 'api' folder exists
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        
        with open(FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)
            
        print(f"Success! Added {len(new_entries)} new links.")
    else:
        print("No new links found.")

except Exception as e:
    print(f"Error occurred: {e}")

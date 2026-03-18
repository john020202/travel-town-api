import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

FILE_PATH = "api/links.json"

# Load existing data
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
else:
    data = []

existing_links = {item['url'] for item in data}
TARGET_URL = "https://simplegameguide.com/travel-town-free-energy/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

new_entries = []

try:
    response = requests.get(TARGET_URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. We look for every link on the page
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True)
        
        # 2. STRICT FILTER: Only grab if it contains 'api.traveltowngame.net'
        # This completely ignores all the #energy-links and social media garbage.
        if 'api.traveltowngame.net' in href:
            if href not in existing_links:
                # We save only the URL and the cleaned energy text
                new_entries.append({
                    "reward_text": text if text else "Free Energy",
                    "url": href,
                    "date_found": datetime.now().isoformat()
                })
                existing_links.add(href)

except Exception as e:
    print(f"Scraper error: {e}")

# 3. Save the clean JSON
if new_entries:
    # Add new ones to the top
    combined_data = new_entries + data
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    with open(FILE_PATH, "w") as f:
        json.dump(combined_data, f, indent=4)
    print(f"Success! Added {len(new_entries)} real reward links.")
else:
    print("No NEW reward links found. All links on the page are already in your JSON.")

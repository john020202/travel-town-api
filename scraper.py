import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

FILE_PATH = "api/links.json"

if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
else:
    data = []

existing_links = {item['url'] for item in data}

TARGET_URLS = [
    "https://simplegameguide.com/travel-town-free-energy/"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

new_entries = []

for url in TARGET_URLS:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # THE ULTIMATE FIX: Only grab links that match the exact structure you provided
            if 'api.traveltowngame.net' in href and href not in existing_links:
                new_entries.append({
                    "url": href,
                    "source_website": url,
                    "date_found": datetime.now().isoformat()
                })
                existing_links.add(href)
                    
    except Exception as e:
        print(f"Error scanning: {e}")

if new_entries:
    data.extend(new_entries)
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
        print(f"Successfully grabbed {len(new_entries)} real reward links!")
else:
    print("No new api.traveltowngame.net links found.")

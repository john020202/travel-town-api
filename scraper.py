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

# The ultimate block list. Nothing from these sites will get through.
BLACKLIST = ['facebook', 'instagram', 'twitter', 'x.com', 'tiktok', 'whatsapp', 't.me', 'reddit', 'apple.com', 'play.google']

new_entries = []

for url in TARGET_URLS:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            link_text = link.text.lower()
            
            # Block all social media and chat apps immediately
            if any(bad in href.lower() for bad in BLACKLIST):
                continue
                
            # If the button visibly says "energy" or "claim" OR the link is a direct API link
            if 'energy' in link_text or 'claim' in link_text or 'traveltowngame.net' in href.lower():
                if href not in existing_links:
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
    
    # THIS is the line that magically recreates your api folder!
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Success! Recreated the API folder and found {len(new_entries)} links.")
else:
    print("No valid links found. The API folder was not created.")

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

# The perfected blacklist to block social media and chat apps
BLACKLIST = [
    'facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'tiktok.com',
    'play.google.com', 'apple.com', 'whatsapp.com', 't.me', 'reddit.com', 'mailto:', '#'
]

new_entries = []

for url in TARGET_URLS:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            link_text = link.text.lower() # We look at the actual button text
            
            # 1. Ignore if it's not a real link or if it's in our blacklist
            if not href.startswith('http') or any(bad in href.lower() for bad in BLACKLIST):
                continue
                
            # 2. THE MAGIC TRICK: Does the button text say "Energy" or "Collect"?
            # Or does the URL explicitly say "traveltown"?
            if 'energy' in link_text or 'collect' in link_text or 'claim' in link_text or 'traveltown' in href.lower():
                
                # If we don't already have it, save it!
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
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

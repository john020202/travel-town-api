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

# We are focusing entirely on the site that works to guarantee success
TARGET_URLS = [
    "https://simplegameguide.com/travel-town-free-energy/"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# This massive blacklist ensures we only grab the raw game reward links
BLACKLIST = [
    'facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'tiktok.com',
    'play.google.com', 'apple.com', 'simplegameguide.com', '#', 'mailto:',
    'youtube.com', 'pinterest.com', 'reddit.com', 'discord.gg', 'whatsapp.com'
]

new_entries = []

for url in TARGET_URLS:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # If it's a real website link and we don't have it yet
            if href.startswith('http') and href not in existing_links:
                
                # Check if it contains any of the bad words in our blacklist
                is_blacklisted = any(bad_word in href.lower() for bad_word in BLACKLIST)
                
                # If it's clean, save it!
                if not is_blacklisted:
                    new_entries.append({
                        "url": href,
                        "source_website": url,
                        "date_found": datetime.now().isoformat()
                    })
                    existing_links.add(href)
                    
    except Exception as e:
        print(f"Error scanning {url}: {e}")

if new_entries:
    data.extend(new_entries)
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

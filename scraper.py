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
    "https://simplegameguide.com/travel-town-free-energy/",
    "https://old.reddit.com/r/TravelTown/search?q=link+OR+energy&restrict_sr=on&sort=new&t=week" 
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# This is our new filter to ignore useless social media links
BLACKLIST = ['facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'tiktok.com', 'play.google.com', 'apple.com']

new_entries = []

for url in TARGET_URLS:
    try:
        print(f"Scanning: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            if 'http' in href.lower() and href not in existing_links:
                # Check if the link contains any of our blacklisted words
                is_blacklisted = any(bad_word in href.lower() for bad_word in BLACKLIST)
                
                # Check if it's an internal blog link
                is_internal = 'simplegameguide.com' in href.lower() or 'reddit.com' in href.lower()
                
                # If it's not blacklisted, not internal, and looks like a reward link, save it!
                if not is_blacklisted and not is_internal:
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
        
    print(f"Success! Sucked up {len(new_entries)} real reward links.")
else:
    print("No new reward links found this time.")

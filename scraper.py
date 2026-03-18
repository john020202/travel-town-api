import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

FILE_PATH = "api/links.json"

# 1. Load existing links so we don't save duplicates
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
else:
    data = []

existing_links = {item['url'] for item in data}

# 2. List of websites to scrape (You can add more here by putting a comma after the quotes)
TARGET_URLS = [
    "https://simplegameguide.com/travel-town-free-energy/",
    # Using old.reddit.com because it is much easier for bots to read than the modern site
    "https://old.reddit.com/r/TravelTown/search?q=link+OR+energy&restrict_sr=on&sort=new&t=week" 
]

# Browsers need a User-Agent so websites don't think we are a bot
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

new_entries = []

# 3. Loop through every website in our list
for url in TARGET_URLS:
    try:
        print(f"Scanning: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        # If the site blocks us, skip to the next one
        if response.status_code != 200:
            print(f"Failed to load {url} - Status Code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find EVERY link on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Check if it's a Travel Town link and we don't already have it
            if 'traveltown' in href.lower() and 'http' in href.lower() and href not in existing_links:
                
                # Prevent scraping internal blog links (like /category/traveltown/)
                if 'simplegameguide.com' not in href.lower() and 'reddit.com' not in href.lower():
                    new_entries.append({
                        "url": href,
                        "source_website": url, # Records where the link came from
                        "date_found": datetime.now().isoformat()
                    })
                    existing_links.add(href)
                    
    except Exception as e:
        print(f"Error scanning {url}: {e}")

# 4. Save the new links to your API folder
if new_entries:
    data.extend(new_entries)
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Success! Sucked up {len(new_entries)} new links.")
else:
    print("No new links found this time.")

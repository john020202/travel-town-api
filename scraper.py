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
TARGET_URL = "https://simplegameguide.com/travel-town-free-energy/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

new_entries = []

try:
    response = requests.get(TARGET_URL, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        raw_text = link.get_text(strip=True) # This grabs the "25 Energy Gift" text
        
        # Block internal site links and social media
        bad_words = ['simplegameguide.com', 'facebook', 'instagram', 'twitter', 'whatsapp', 't.me', 'reddit']
        if any(bad in href.lower() for bad in bad_words):
            continue
            
        # If it has the API url OR the text says "Energy"
        if 'api.traveltowngame.net' in href or 'energy' in raw_text.lower():
            if href not in existing_links:
                
                # Clean up the text (removes the "1. " from "1. 25 Energy Gift")
                clean_text = raw_text.split('. ')[-1] if '. ' in raw_text else raw_text
                if not clean_text or clean_text == "":
                    clean_text = "Claim Free Energy"
                    
                new_entries.append({
                    "text": clean_text, # Saves the text to your database!
                    "url": href,
                    "date_found": datetime.now().isoformat()
                })
                existing_links.add(href)
                
except Exception as e:
    print(f"Error: {e}")

if new_entries:
    data.extend(new_entries)
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Success! Grabbed {len(new_entries)} links with their text.")
else:
    print("No new links found.")

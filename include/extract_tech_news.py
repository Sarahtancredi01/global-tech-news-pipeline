import requests
import json
import os

def extract_tech_news(**kwargs):
    # 1. Get top story IDs
    top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_ids = requests.get(top_ids_url).json()[:20] 
    
    stories = []
    for s_id in top_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
        stories.append(requests.get(item_url).json())
    
    # CHANGE: Save to a local file in your project folder instead of /tmp/
    # This creates the file in the 'include' folder specifically
    base_path = os.path.dirname(__file__)
    raw_path = os.path.join(base_path, "extracted_news.csv") # We'll save as CSV to match your transform script
    
    # We'll use pandas to save it as a CSV so your transform script can read it easily
    import pandas as pd
    df = pd.DataFrame(stories)
    df.to_csv(raw_path, index=False)
    
    return raw_path

# FIX: This block must be at the very edge of the left margin (not indented)
if __name__ == "__main__":
    extract_tech_news()
    print("--- SUCCESS: Tech News Extracted to include/extracted_news.csv! ---")
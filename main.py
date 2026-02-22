import os
import json
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables from the .env file
load_dotenv()

# 1. Setup your Apify Token and the Actor ID securely
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
ACTOR_ID = os.getenv("ACTOR_ID")

# Safety check to ensure the .env file was read correctly
if not APIFY_API_TOKEN or not ACTOR_ID:
    print("Error: Missing API credentials. Please check your .env file.")
    exit()

# Initialize the Apify client
client = ApifyClient(APIFY_API_TOKEN)

# 2. Prepare the Input based on the documentation
run_input = {
    "mode": "products",
    "countryCode": "US",
    "categoryId": "12472",  # sub-cateory id e.g Women's Dresses 
    "page": 1,              # Start at page 1
    "perPage": 100          # Get the maximum 100 products per page
}

print(f"Starting Apify Shein Scraper for Category {run_input['categoryId']}...")

try:
    # 3. Run the Actor and wait for it to finish
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    
    print("Scraping finished! Downloading the data...")

    # 4. Fetch the results from Apify's cloud dataset
    all_products = []
    
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if "products" in item:
            all_products.extend(item["products"])
        else:
            all_products.append(item)

    # 5. Save the exact JSON output to a file
    if all_products:
        filename = f"shein_category_{run_input['categoryId']}.json"
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(all_products, file, indent=4, ensure_ascii=False)
            
        print(f"✅ Success! Saved {len(all_products)} products to '{filename}'")
    else:
        print("The scraper ran, but no products were found.")

except Exception as e:
    print(f"An error occurred while running the Apify Actor: {e}")
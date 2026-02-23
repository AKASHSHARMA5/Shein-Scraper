import json
import time
import random
from DrissionPage import ChromiumPage, ChromiumOptions

def scrape_deep_details():
    # 1. Load the data you already saved
    try:
        with open('shein_flawless.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("❌ Could not find 'shein_flawless.json'. Make sure it's in the same folder.")
        return

    print(f"📦 Loaded {len(products)} products. Starting deep scrape for the first 3...")
    
    # ==========================================
    # 🛑 YOUR WEBSHARE PROXY SETUP 🛑
    # Put the EXACT SAME IP:PORT here that you used in Script 1!
    # Example format: '185.199.229.156:8080'
    # ==========================================
    my_proxy = '31.59.20.176:6754'
    
    # --- LEVEL 1 PROTECTION: USER-AGENT ROTATION ---
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.0.0 Safari/537.36"
    ]
    
    # Configure the browser with Proxy, Image Blocking, and User Agent
    co = ChromiumOptions()
    co.set_proxy(my_proxy)
    co.no_imgs(True) # CRITICAL: Saves your 1GB free bandwidth!
    co.set_user_agent(random.choice(user_agents))
    
    page = ChromiumPage(co)
    
    # 2. Loop through the URLs (Limiting to 3 for safe testing)
    for index, product in enumerate(products[:3]):
        url = product['url']
        print(f"\n[{index + 1}/3] Visiting via Proxy: {product['name']}")
        
        page.get(url)
        
        # --- LEVEL 1 PROTECTION: RANDOMIZED DELAYS ---
        sleep_time = random.uniform(4.5, 8.2)
        print(f"   ⏳ Waiting {sleep_time:.2f} seconds to mimic human reading...")
        time.sleep(sleep_time) 
        
        # --- LEVEL 1 PROTECTION: HUMAN SCROLLING ---
        page.scroll.down(random.randint(300, 700))
        time.sleep(random.uniform(1.0, 2.5)) 
        
        # 3. Extract the deep details
        try:
            details_div = page.ele('xpath://div[contains(@class, "product-intro")]', timeout=3)
            
            if details_div:
                raw_text = details_div.text
                clean_text = "\n".join([line for line in raw_text.split('\n') if line.strip()])
                product['deep_details'] = clean_text
                print("   ✅ Successfully extracted details.")
            else:
                product['deep_details'] = "Details block not found."
                print("   ⚠️ Could not find the details block on this page.")
                
        except Exception as e:
            product['deep_details'] = f"Error: {e}"
            print("   ❌ Error extracting details.")

    # 4. Save the enriched data to a new file
    with open("shein_enriched_data.json", "w", encoding="utf-8") as f:
        json.dump(products[:3], f, indent=4)
        
    print("\n🎉 Done! Check 'shein_enriched_data.json' for the deep details.")
    page.quit()

if __name__ == "__main__":
    scrape_deep_details()
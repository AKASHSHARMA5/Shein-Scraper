import json
import time
import random
from DrissionPage import ChromiumPage, ChromiumOptions

# ==========================================
# 🛑 CONFIGURATION 🛑
# ==========================================
MY_PROXY = '23.95.150.145:6114' 
RESET_EVERY_X_ITEMS = 15  # Wipe session every 15 products to stay under the radar
SAVE_PROGRESS_EVERY = 50   # Emergency save every 50 items

def create_fresh_browser():
    """Launch a clean browser instance with rotated identity."""
    print("\n♻️  Resetting session and clearing cookies...")
    co = ChromiumOptions()
    co.set_proxy(MY_PROXY)
    co.no_imgs(True)  # CRITICAL: Saves massive bandwidth for 5,000 pages
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    co.set_user_agent(random.choice(user_agents))
    return ChromiumPage(co)

def scrape_deep_details():
    # 1. Load the 5,000 products from Script 1
    try:
        with open('shein_flawless.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'shein_flawless.json' not found.")
        return

    total_count = len(products)
    print(f"📦 Loaded {total_count} products. Starting deep scrape...")
    
    page = create_fresh_browser()
    
    try:
        # 2. Process ALL products
        for index, product in enumerate(products):
            
            # --- STRATEGY: PROACTIVE SESSION RESET ---
            if index > 0 and index % RESET_EVERY_X_ITEMS == 0:
                print(f"🛠  Reached {index} items. Rebooting browser to lower Bot Score...")
                page.quit()
                time.sleep(random.uniform(5, 10))
                page = create_fresh_browser()

            print(f"[{index + 1}/{total_count}] Visiting: {product['name']}")
            
            try:
                page.get(product['url'])
                
                # --- STRATEGY: RANDOM HUMAN DELAYS ---
                time.sleep(random.uniform(4.0, 7.0))
                
                # Check for Captcha/Block (If product intro is missing)
                details_div = page.ele('xpath://div[contains(@class, "product-intro")]', timeout=3)
                
                if not details_div:
                    print("⚠️  Empty page or Captcha! Attempting Hard Refresh...")
                    page.refresh()
                    time.sleep(8)
                    details_div = page.ele('xpath://div[contains(@class, "product-intro")]')

                if details_div:
                    raw_text = details_div.text
                    # Clean up the text
                    clean_text = "\n".join([line for line in raw_text.split('\n') if line.strip()])
                    product['deep_details'] = clean_text
                    print("   ✅ Details saved.")
                else:
                    product['deep_details'] = "Blocked or Not Found"
                    print("   ❌ Failed to load details.")

            except Exception as e:
                print(f"   ❌ Error: {e}")
                product['deep_details'] = "Error during scrape"

            # --- STRATEGY: PERIODIC AUTO-SAVE ---
            if (index + 1) % SAVE_PROGRESS_EVERY == 0:
                with open("shein_deep_progress.json", "w", encoding="utf-8") as f:
                    json.dump(products[:index+1], f, indent=4)
                print(f"💾 Progress checkpoint: {index + 1} items saved.")

    finally:
        # 3. Final Save
        print("\n💾 Saving final data...")
        with open("shein_final_enriched.json", "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4)
        print(f"🎉 MISSION COMPLETE! Check 'shein_final_enriched.json'.")
        page.quit()

if __name__ == "__main__":
    scrape_deep_details()
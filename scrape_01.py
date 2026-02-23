import json
import time
import re
import random
from urllib.parse import urlparse
from DrissionPage import ChromiumPage, ChromiumOptions

# ==========================================
# 🛑 CONFIGURATION 🛑
# ==========================================
MY_PROXY = '23.95.150.145:6114'
BASE_URL = "https://us.shein.com/category-c-12472.html"
PAGES_BEFORE_RESTART = 4  # Lower this to 2 or 3 if you still see Captchas

def create_fresh_browser():
    """Launch a brand new browser instance to reset Bot Score."""
    print("\n♻️  Creating a fresh browser session to clear trackers...")
    co = ChromiumOptions()
    co.set_proxy(MY_PROXY)
    
    # Randomize User-Agent to look like a different person each time
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.0.0 Safari/537.36"
    ]
    co.set_user_agent(random.choice(ua_list))
    return ChromiumPage(co)

def get_flawless_product_details():
    all_extracted_products = []
    current_page_num = 1 
    page = create_fresh_browser()

    try:
        print("🚀 Launching Ironclad Scraper with Auto-Reset...")
        
        while True:
            # --- STRATEGY 1: PROACTIVE SESSION RESET ---
            # Every few pages, we kill the browser before a Captcha even has a chance to appear
            if current_page_num > 1 and (current_page_num - 1) % PAGES_BEFORE_RESTART == 0:
                print(f"🛠  Safety Reset: Reaching Page {current_page_num}. Refreshing identity...")
                page.quit()
                time.sleep(random.uniform(7, 12)) 
                page = create_fresh_browser()

            print(f"\n📄 --- SCRAPING PAGE {current_page_num} ---")
            
            # --- STRATEGY 2: DIRECT URL INJECTION ---
            target_url = f"{BASE_URL}?page={current_page_num}"
            print(f"🔗 Navigating directly to: {target_url}")
            page.get(target_url)
            
            # Human-like loading wait
            time.sleep(random.uniform(5.0, 8.0))

            print("⏬ Scrolling to trigger lazy-loading...")
            for _ in range(5): 
                page.scroll.down(1000)
                time.sleep(random.uniform(2.0, 3.5))
                
            links = page.eles('xpath://a[contains(@href, "-p-")]')
            
            # --- STRATEGY 3: REACTIVE CAPTCHA RESCUE ---
            # If we find 0 products, we assume a Captcha/Block and restart immediately
            if len(links) == 0:
                print("⚠️ WARNING: Found 0 products! Likely a CAPTCHA wall.")
                print("📸 Saving error log screenshot...")
                page.get_screenshot(path=f"captcha_at_page_{current_page_num}.jpg")
                
                print("🔄 Executing Emergency Reset Rescue...")
                page.quit()
                cool_down = random.randint(30, 60)
                print(f"⏳ Cooling down for {cool_down} seconds before retrying...")
                time.sleep(cool_down)
                
                page = create_fresh_browser()
                continue # Retries the SAME page number with a fresh identity

            # --- EXTRACTION LOGIC ---
            products_dict = {}
            for link in links:
                href = link.attr('href')
                if not href: continue
                url = href if href.startswith('http') else f"https://us.shein.com{href}"
                
                if url not in products_dict:
                    products_dict[url] = {"name": "", "price": "", "image": "", "url": url}
                
                # Name Extraction
                try:
                    path = urlparse(url).path
                    raw_slug = path.split('-p-')[0].strip('/')
                    products_dict[url]["name"] = raw_slug.replace('-', ' ').title()
                except: pass

                # Image Extraction
                try:
                    img_tag = link.ele('tag:img', timeout=0.5)
                    if img_tag:
                        src = img_tag.attr('src')
                        data_src = img_tag.attr('data-src')
                        products_dict[url]["image"] = data_src if (src and 'bg-grey' in src) else (src or data_src)
                except: pass

                # Price Extraction
                try:
                    parent = link.parent(2) 
                    prices = re.findall(r'\$\d+\.\d{2}', parent.text)
                    if prices: products_dict[url]["price"] = prices[0]
                except: pass

            page_valid_count = 0
            for url, data in products_dict.items():
                if data["name"] and data["price"]:
                    all_extracted_products.append(data)
                    page_valid_count += 1
            
            print(f"✅ Successfully grabbed {page_valid_count} products.")
            
            # Move to next page
            current_page_num += 1
            time.sleep(random.uniform(4, 7))

    except Exception as e:
        print(f"❌ Critical Error: {e}")
    finally:
        # Final Save
        print("\n💾 Saving all collected data to 'shein_flawless.json'...")
        with open("shein_flawless.json", "w", encoding="utf-8") as f:
            json.dump(all_extracted_products, f, indent=4)
        print(f"🎉 Process Finished. Total items: {len(all_extracted_products)}")
        page.quit()

if __name__ == "__main__":
    get_flawless_product_details()
import json
import time
import random
import os
import shutil
from DrissionPage import ChromiumPage, ChromiumOptions

# ==========================================
# 🛑 CONFIGURATION 🛑
# ==========================================
# Broken down proxy credentials for the extension generator
PROXY_HOST = "p.webshare.io"
PROXY_PORT = 80
PROXY_USER = "jocvykbwresidential-8"
PROXY_PASS = "c2m6ic09of3q"

RESET_EVERY_X_ITEMS = 15   # Wipe session every 15 products to stay under the radar
SAVE_PROGRESS_EVERY = 50   # Emergency save every 50 items

def build_proxy_extension():
    """Builds a temporary Chrome Extension to silently inject the proxy password."""
    ext_dir = os.path.join(os.getcwd(), 'auto_proxy_plugin_2')
    
    if os.path.exists(ext_dir): 
        shutil.rmtree(ext_dir)
    os.makedirs(ext_dir)
    
    manifest = """{
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Silent Proxy Auth 2",
        "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"],
        "background": {"scripts": ["bg.js"]},
        "minimum_chrome_version": "22.0.0"
    }"""
    
    bg_js = f"""
    var config = {{ mode: "fixed_servers", rules: {{ singleProxy: {{ scheme: "http", host: "{PROXY_HOST}", port: {PROXY_PORT} }}, bypassList: ["localhost"] }} }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{ return {{ authCredentials: {{ username: "{PROXY_USER}", password: "{PROXY_PASS}" }} }}; }},
        {{urls: ["<all_urls>"]}}, ['blocking']
    );
    """
    with open(os.path.join(ext_dir, "manifest.json"), "w") as f: f.write(manifest)
    with open(os.path.join(ext_dir, "bg.js"), "w") as f: f.write(bg_js)
    
    return ext_dir

def create_fresh_browser():
    """Launch a clean browser instance with rotated identity."""
    print("\n♻️  Resetting session and clearing cookies...")
    co = ChromiumOptions()
    
    # 🚨 Inject the background proxy extension
    proxy_folder = build_proxy_extension()
    co.add_extension(proxy_folder)
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.0.0 Safari/537.36"
    ]
    co.set_user_agent(random.choice(user_agents))
    return ChromiumPage(co)

def scrape_deep_details():
    try:
        with open('shein_flawless.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'shein_flawless.json' not found. Run script 1 first!")
        return

    total_count = len(products)
    print(f"📦 Loaded {total_count} products. Starting deep scrape...")
    
    page = create_fresh_browser()
    
    index = 0
    last_reset_index = -1

    try:
        # Using a WHILE loop so we can retry the exact same product if we get blocked
        while index < total_count:
            product = products[index]
            
            # --- STRATEGY: PROACTIVE SESSION RESET ---
            if index > 0 and index % RESET_EVERY_X_ITEMS == 0 and index != last_reset_index:
                print(f"🛠  Reached {index} items. Rebooting browser to lower Bot Score...")
                page.quit()
                time.sleep(random.uniform(5, 10))
                page = create_fresh_browser()
                last_reset_index = index

            print(f"\n[{index + 1}/{total_count}] Visiting: {product['name']}")
            
            try:
                page.get(product['url'])
                time.sleep(random.uniform(4.0, 7.0))
                
                # 🚨 NEW: THE RISK DETECTOR 🚨
                if "risk/action/limit" in page.url or "403" in page.html:
                    print("🛑 HIT THE RISK WALL! Rotating IP...")
                    page.quit()
                    time.sleep(random.randint(15, 25))
                    page = create_fresh_browser()
                    continue # Retries the EXACT SAME product index!

                # Check for Captcha/Block (If product intro is missing)
                details_div = page.ele('xpath://div[contains(@class, "product-intro")]', timeout=3)
                
                if not details_div:
                    print("⚠️  Empty page or Captcha! Attempting Hard Refresh...")
                    page.refresh()
                    time.sleep(8)
                    details_div = page.ele('xpath://div[contains(@class, "product-intro")]')

                if details_div:
                    raw_text = details_div.text
                    clean_text = "\n".join([line for line in raw_text.split('\n') if line.strip()])
                    product['deep_details'] = clean_text
                    print("   ✅ Details saved.")
                else:
                    product['deep_details'] = "Blocked or Not Found"
                    print("   ❌ Failed to load details.")

            except Exception as e:
                print(f"   ❌ Error: {e}")
                product['deep_details'] = "Error during scrape"

            # Move to the next product only if we didn't hit a `continue` (risk wall)
            index += 1

            # --- STRATEGY: PERIODIC AUTO-SAVE ---
            if index % SAVE_PROGRESS_EVERY == 0:
                with open("shein_deep_progress.json", "w", encoding="utf-8") as f:
                    json.dump(products[:index], f, indent=4)
                print(f"💾 Progress checkpoint: {index} items saved.")

    finally:
        print("\n💾 Saving final data...")
        with open("shein_final_enriched.json", "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4)
        print(f"🎉 MISSION COMPLETE! Check 'shein_final_enriched.json'.")
        try:
            page.quit()
        except:
            pass

if __name__ == "__main__":
    scrape_deep_details()
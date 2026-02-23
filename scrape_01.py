from DrissionPage import ChromiumPage, ChromiumOptions
from urllib.parse import urlparse
import json
import time
import re

def get_flawless_product_details():
    print("🚀 Configuring browser with Webshare proxy...")
    
    # ==========================================
    # 🛑 YOUR WEBSHARE PROXY SETUP 🛑
    # REPLACE THE STRING BELOW WITH YOUR ACTUAL WEBSHARE DETAILS!
    # Format: 'username:password@ip:port'
    # ==========================================
    my_proxy = '31.59.20.176:6754'
    
    co = ChromiumOptions()
    co.set_proxy(my_proxy)
    co.no_imgs(True) # Blocks image downloads to save your 1GB of bandwidth!
    
    # Pass the options to the browser
    page = ChromiumPage(co)
    
    try:
        print("🚀 Launching browser...")
        page.get("https://us.shein.com/category-c-12472.html")
        time.sleep(6) # Wait a little extra time for proxy routing
        
        # Scroll deliberately to force images to load
        print("⏬ Scrolling to trigger lazy-loading...")
        for _ in range(3):
            page.scroll.down(1500)
            time.sleep(2)
            
        products_dict = {}
        links = page.eles('xpath://a[contains(@href, "-p-")]')
        
        print(f"🔍 Analyzing {len(links)} product nodes...")
        
        for link in links:
            href = link.attr('href')
            if not href: continue
            
            url = href if href.startswith('http') else f"https://us.shein.com{href}"
            
            if url not in products_dict:
                products_dict[url] = {"name": "", "price": "", "image": "", "url": url}
            
            # 1. PERFECT NAME: Extract from the URL itself
            try:
                path = urlparse(url).path
                raw_slug = path.split('-p-')[0].strip('/')
                clean_name = raw_slug.replace('-', ' ').title()
                products_dict[url]["name"] = clean_name
            except:
                pass

            # 2. PERFECT IMAGE: Bypass the gray placeholder
            if not products_dict[url]["image"]:
                try:
                    img_tag = link.ele('tag:img', timeout=0)
                    if img_tag:
                        # Grab both potential image sources
                        src = img_tag.attr('src')
                        data_src = img_tag.attr('data-src')
                        
                        # Use data-src if the main src is the gray placeholder
                        final_src = data_src if (src and 'bg-grey' in src) else (src or data_src)
                        
                        if final_src and 'http' in final_src and 'bg-grey' not in final_src:
                            products_dict[url]["image"] = final_src
                except:
                    pass

            # 3. PERFECT PRICE: Use Regex to find the exact dollar amount
            if not products_dict[url]["price"]:
                try:
                    parent = link.parent(2) 
                    text_content = parent.text
                    # Find all matches that look like $XX.XX
                    prices = re.findall(r'\$\d+\.\d{2}', text_content)
                    if prices:
                        # Grab the first valid price found in that block
                        products_dict[url]["price"] = prices[0]
                except:
                    pass

        # Validate and filter
        final_products = []
        for url, data in products_dict.items():
            # Only keep the product if it successfully grabbed all 3 pieces of data
            if data["name"] and data["price"] and data["image"]:
                final_products.append(data)
            
            if len(final_products) >= 40:
                break

        with open("shein_flawless.json", "w", encoding="utf-8") as f:
            json.dump(final_products, f, indent=4)
            
        print(f"✅ SUCCESS! Saved {len(final_products)} perfect products.")
        print("📁 Open 'shein_flawless.json' to check the results!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        page.quit()

if __name__ == "__main__":
    get_flawless_product_details()
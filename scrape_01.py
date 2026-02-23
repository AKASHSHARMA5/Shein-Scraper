from DrissionPage import ChromiumPage
import json
import time

def diagnostic_scrape():
    page = ChromiumPage()
    
    try:
        print("🚀 Launching browser...")
        page.get("https://us.shein.com/category-c-12472.html")
        
        # Wait 5 seconds for any popups or security checks to finish loading
        time.sleep(5)
        
        # 1. VISUAL DEBUGGING: Take a picture of what the browser sees
        page.get_screenshot(path="debug_screenshot.jpg")
        print("📸 Saved 'debug_screenshot.jpg'. (Check this image if it fails again!)")
        
        print("🔍 Hunting for products using high-speed XPath...")
        products = []
        
        # 2. XPATH SEARCH: Instantly find all links containing '-p-' (Product links)
        # This executes inside the browser engine, making it incredibly fast
        product_links = page.eles('xpath://a[contains(@href, "-p-")]')
        
        for link in product_links:
            href = link.attr('href')
            # Grab the title attribute or the text inside the link
            name = link.attr('title') or link.text
            
            # Filter out empty links or tiny fragments
            if href and name and len(name.strip()) > 5:
                # Prevent duplicates
                if not any(p['url'] == href for p in products):
                    products.append({
                        "name": name.strip(),
                        "url": href if href.startswith('http') else f"https://us.shein.com{href}"
                    })
            
            # Stop at 40 so we don't overload anything during testing
            if len(products) >= 40:
                break

        # Save the results
        with open("shein_final.json", "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4)
            
        print(f"✅ SUCCESS! Saved {len(products)} products to shein_final.json")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
    finally:
        page.quit()

if __name__ == "__main__":
    diagnostic_scrape()
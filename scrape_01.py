from DrissionPage import ChromiumPage
import json
import time

def get_full_product_details():
    page = ChromiumPage()
    
    try:
        print("🚀 Launching browser and navigating to SHEIN...")
        page.get("https://us.shein.com/category-c-12472.html")
        
        # Wait for the page to initialize
        time.sleep(4)
        
        # Scroll down to force the images and prices to load (Lazy Loading)
        print("⏬ Scrolling to load images and prices...")
        page.scroll.down(3000)
        time.sleep(3)
        
        # We use a dictionary to group data by URL so we don't get duplicates
        products_dict = {}
        
        print("📸 Scanning page for Images, Prices, and Names...")
        
        # Find all product links
        links = page.eles('xpath://a[contains(@href, "-p-")]')
        
        for link in links:
            href = link.attr('href')
            if not href: continue
            
            url = href if href.startswith('http') else f"https://us.shein.com{href}"
            
            # Create a blank slate for the product if it's new
            if url not in products_dict:
                products_dict[url] = {"name": "", "price": "", "image": "", "url": url}
            
            # 1. --- EXTRACT CLEAN NAME ---
            # The 'title' attribute usually holds the perfectly clean name
            title_attr = link.attr('title')
            if title_attr and len(title_attr) > 5:
                products_dict[url]["name"] = title_attr
            elif not products_dict[url]["name"] and link.text:
                # Fallback: Clean the text by removing discounts and "Save $" lines
                lines = link.text.split('\n')
                for line in lines:
                    line = line.strip()
                    if len(line) > len(products_dict[url]["name"]) and "$" not in line and "%" not in line and line.lower() != 'local':
                        products_dict[url]["name"] = line

            # 2. --- EXTRACT IMAGE ---
            if not products_dict[url]["image"]:
                # Look for an image tag inside this link
                img_tag = link.ele('tag:img', timeout=0)
                if img_tag:
                    # Sometimes websites use data-src for lazy loading
                    src = img_tag.attr('src')
                    if src and 'data:image' in src: 
                        src = img_tag.attr('data-src') or src
                        
                    if src and 'http' in src:
                        products_dict[url]["image"] = src

            # 3. --- EXTRACT PRICE ---
            if not products_dict[url]["price"]:
                try:
                    # Go UP the HTML tree to the product container, then search for the $ sign
                    parent = link.parent(2) 
                    price_ele = parent.ele('text:$', timeout=0)
                    if price_ele:
                        # Grab just the line with the current price (ignoring crossed-out old prices)
                        raw_lines = price_ele.text.split('\n')
                        for line in raw_lines:
                            if '$' in line:
                                products_dict[url]["price"] = line.strip()
                                break
                except:
                    pass

        # Filter out any items that didn't get a full set of data
        final_products = []
        for url, data in products_dict.items():
            if data["name"] and data["price"] and data["image"]:
                final_products.append(data)
            
            # Stop when we have 40 perfect products
            if len(final_products) >= 40:
                break

        # Save to file
        with open("shein_full_details.json", "w", encoding="utf-8") as f:
            json.dump(final_products, f, indent=4)
            
        print(f"✅ SUCCESS! Extracted {len(final_products)} complete products.")
        print("📁 Open 'shein_full_details.json' to see your clean data!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        page.quit()

if __name__ == "__main__":
    get_full_product_details()
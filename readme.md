# SHEIN Category Scraper: Women's Dresses

This project is a Python-based web scraping solution designed to extract structured product data from SHEIN's specific product categories (e.g., Women's Dresses, Category ID: 12472). 

It safely extracts comprehensive product details—including real-time pricing, stock availability, and high-resolution image URLs—and exports the data into a clean, analytical JSON format.

## Design Choices: Why Apify instead of Selenium?

For this task, I architected the solution to use the Apify platform and its Python Client rather than building a custom Selenium or Playwright script from scratch. This decision was made for several critical engineering and reliability reasons:

1. Advanced Anti-Bot Evasion (WAF Bypass): SHEIN employs aggressive Web Application Firewalls (WAF) and bot-mitigation systems (like Cloudflare and DataDome). Standard Selenium instances have easily identifiable browser fingerprints that immediately trigger CAPTCHAs or `503 Service Unavailable` blocks. Apify seamlessly handles browser fingerprint spoofing to mimic genuine user traffic.

2. Built-in Proxy Rotation: Scraping thousands of products requires rotating residential proxies. Instead of purchasing, configuring, and managing a complex proxy pool locally with Selenium, Apify handles proxy rotation natively to prevent IP bans.

3. Speed and Scalability: Selenium is heavy and computationally expensive to run locally, especially when loading images and executing JavaScript. By utilizing an Apify cloud actor, the heavy lifting is offloaded, allowing for much faster, asynchronous data extraction.

4. Maintainability: E-commerce sites frequently change their DOM structures. Relying on an API-driven scraping structure reduces the maintenance debt of constantly updating XPath or CSS selectors when SHEIN updates its UI.

## Prerequisites

• Python 3.6+  
• An Apify account (the free tier provides sufficient compute credits for this extraction).

## Installation & Setup

1. Clone or download this repository.  
2. Open your terminal and install the required Apify Python client:

   pip install apify-client

3. Obtain your Apify API Token:

   Log into Apify and navigate to Settings > Integrations.  
   Copy your Personal API token.

## Configuration

Before running the script, update the authentication and targeting variables at the top of the scraper.py file:

• APIFY_API_TOKEN: Insert your personal token here.  
• ACTOR_ID: The unique identifier of the SHEIN scraper on the Apify store.  
• categoryId: Set to "12472" to specifically target the Women's Dresses category.

## Usage

Once your environment variables are configured, execute the script via the command line:

python scraper.py

## Modifying the Scrape Parameters

You can adjust the run_input dictionary within the script to customize the extraction:

• "page": The starting pagination number (default: 1).  
• "perPage": Items extracted per page (maximum: 100).  
• "countryCode": Regional marketplace targeting (e.g., "US", "GB").

## Output Structure

The script outputs a highly structured JSON file (e.g., shein_apify_category_12472.json) to your local directory. Each product entry contains deep data points, including:

• goods_id / goods_name: Unique identifiers and full product titles.  
• retailPrice & discountPrice: Current and historical pricing metrics.  
• stock & realStock: Frontend display stock vs. actual warehouse inventory.  
• main_image & detail_image: Direct URLs to all product media.  
• productUrl: Direct storefront link.
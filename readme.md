# 👗 SHEIN Ironclad Scraper – Women's Dresses (Category ID: 12472)

A high-performance, two-stage Python scraping system engineered to extract structured product data from SHEIN’s **Women's Dresses** category.

Built with a custom **“Ironclad” anti-block architecture**, this scraper is designed to withstand aggressive bot detection systems through intelligent session resets, browser fingerprint control, and bandwidth optimization.

---

## 🏗 System Architecture – Two-Stage Pipeline

To maximize **speed, stability, and scalability**, the system is divided into two specialized scripts:

---

### 🔹 Stage 1: Category Harvester (`scrape_01.py`)

**Purpose:** Crawl category listing pages and collect foundational product data.

**Extracts:**
- Product URLs  
- Product names  
- Base prices  
- Thumbnail image URLs  

**Output File:**
```
shein_flawless.json  (currently contains approx 5000 scrape shein product data)
```

---

### 🔹 Stage 2: Deep Detail Scraper (`scrape_02.py`)

**Purpose:** Visit each product URL collected in Stage 1 and extract enriched product details.

**Extracts:**
- Full raw product text (descriptions, materials, sizes)
- Pricing variations & discounts
- SKU numbers
- Structured intro-page data block

**Features:**
- Auto-save checkpoint system (`shein_deep_progress.json`)
- Crash-safe recovery logic

**Output File:**
```
shein_final_enriched.json
```
or
```
shein_enriched_data.json
```

---

## 🛠 Engineering Decision – Why DrissionPage?

This version was rebuilt using **DrissionPage** instead of Selenium or Apify for superior stealth and performance.

### ✅ Hybrid Control
- Combines requests-level speed with full Chromium rendering power  
- Handles dynamic JavaScript efficiently  
- Lighter and faster than Selenium  

### ✅ WAF & Fingerprint Resistance
- Avoids `webdriver: true` detection flags  
- Less detectable by WAF systems (e.g., Akamai, Cloudflare)  
- Reduces “Access Denied” errors  

### ✅ Manual Override & Recovery Logic
- Hard Refresh Rescue mechanism  
- Automatic session reset on CAPTCHA detection  
- Cookie clearing & browser identity refresh  

---

## 🛡 Anti-Block Strategy (Ironclad Method)

### 🔁 Intelligent Session Reset  
Resets the browser session every **15 products** to prevent behavioral profiling and tracking accumulation.

### 🔗 Direct URL Pagination  
Injects page parameters directly into the URL, bypassing tracked “Next Page” button events.

### ⚡ Bandwidth Optimization  
Blocks image loading using:
```python
co.no_imgs(True)
```
- Reduces proxy bandwidth usage  
- Improves page load speeds by up to **5×**

---

## 🚀 Installation & Setup

### 📌 Prerequisites
- Python 3.8+
- Chromium-based browser (Google Chrome or Microsoft Edge)

---

### 📦 Install Dependencies

```bash
pip install DrissionPage
```

---

### 🌐 Proxy Configuration

Update the `MY_PROXY` variable inside both scripts with your proxy credentials:

```
IP:PORT
```

> Recommended: Rotating residential proxies for large-scale scraping.

---

## ▶ Usage

### 1️⃣ Run Category Harvester

```bash
python scrape_01.py
```

**Output:** `shein_flawless.json`

---

### 2️⃣ Run Deep Detail Scraper

```bash
python scrape_02.py
```

**Output:** `shein_final_enriched.json`

---

## 📊 Final Output Structure (JSON)

### 🔹 Stage 1 Output – `shein_flawless.json`

```json
{
  "name": "Elenzga Women S Front Tie Short Sleeve Printed Casual Fitted Dress",
  "price": "$14.33",
  "image": "https://img.ltwebstatic.com/images3_pi/2024/12/26/e8/1735207340235828ef478c01041fe12fd3a23cb8f5_thumbnail_600x.webp",
  "url": "https://us.shein.com/Elenzga-Women-s-Front-Tie-Short-Sleeve-Printed-Casual-Fitted-Dress-p-51609535.html?mallCode=1&pageListType=4"
}
```

---

### 🔹 Stage 2 Output – `shein_final_enriched.json`

```json
{
  "name": "Women S Boho Style Sleeveless Asymmetrical Loose Floral Print Dress Casual Summer Dress Suitable For Various Body Types",
  "price": "$7.42",
  "image": "https://img.ltwebstatic.com/images3_spmp/2025/03/19/cb/1742374616c2c62ac921e8a98dc1ab6f97cd6f6524_thumbnail_600x.webp",
  "url": "https://us.shein.com/Women-s-Boho-Style-Sleeveless-Asymmetrical-Loose-Floral-Print-Dress-Casual-Summer-Dress-Suitable-For-Various-Body-Types-p-57849616.html?mallCode=1&pageListType=4",
  "deep_details": "Full raw product intro text including SKU, description, size guide, pricing variations, store info, and customer sections..."
}
```

---

## ⚠ Disclaimer

This project is intended strictly for:
- Educational purposes  
- Research  
- Data engineering practice  

Ensure compliance with SHEIN’s Terms of Service and all applicable laws before deploying at scale.

---

## 📌 Key Highlights

✔ Two-Stage Scalable Architecture  
✔ CAPTCHA Recovery Logic  
✔ Smart Session Rotation  
✔ Optimized Proxy Usage  
✔ Clean Analytical JSON Output  
✔ Crash-Safe Progress Tracking  

---

## 💡 Summary

**Built for performance. Engineered for resilience. Designed for scale.**

The Ironclad architecture ensures maximum extraction efficiency while minimizing detection risk — making it suitable for controlled, research-grade scraping workflows.
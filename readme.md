# 👗 SHEIN Ironclad Scraper – Women's Dresses (Category ID: 12472)

A high-performance, two-stage Python scraping system engineered to extract products from SHEIN’s Women's Dresses category.

Built with a custom **“Ironclad” anti-block architecture**, this scraper is designed to handle aggressive bot detection systems using intelligent session resets, browser fingerprint control, and bandwidth optimization.

---

## 🏗 System Architecture – Two-Stage Pipeline

To maximize speed, stability, and scalability, the scraper is divided into two specialized scripts:

### 🔹 Stage 1: Category Harvester (`script1_harvester.py`)
- Crawls category listing pages
- Collects:
  - Product URLs  
  - Product names  
  - Base prices  
- Generates initial dataset file:  
  `shein_flawless.json`

---

### 🔹 Stage 2: Deep Detail Scraper (`script2_deep_details.py`)
- Visits each product URL collected in Stage 1
- Extracts:
  - Full descriptions  
  - Materials & composition  
  - Intro text  
  - High-resolution image URLs  
- Includes auto-save checkpoint system:
  `shein_deep_progress.json`

---

## 🛠 Engineering Decision – Why DrissionPage?

This version was rebuilt using **DrissionPage** instead of Selenium or Apify for better stealth and performance.

### ✅ Hybrid Control
Combines:
- Requests-level speed
- Full Chromium rendering power

Handles dynamic JavaScript efficiently while remaining lighter than Selenium.

### ✅ WAF & Fingerprint Resistance
- Avoids `webdriver: true` flags
- Less detectable by WAF systems (e.g., Akamai)
- Reduces “Access Denied” blocks

### ✅ Manual Override & Recovery Logic
Includes:
- Hard Refresh Rescue mechanism
- Automatic Session Reset
- Cookie clearing on CAPTCHA detection
- Browser restart with fresh identity

---

## 🛡 Anti-Block Strategy (Ironclad Method)

### 🔁 Intelligent Session Reset
- Browser session reset every 15 products
- Clears cookies & tracking data
- Prevents behavioral profiling

### 🔗 Direct URL Pagination
- Injects page parameters directly
- Bypasses tracked “Next Page” buttons

### ⚡ Bandwidth Optimization
- Blocks image loading (`co.no_imgs(True)`)
- Reduces proxy bandwidth usage
- Improves page load speed significantly

---

## 🚀 Installation & Setup

### 📌 Prerequisites
- Python 3.8+
- Chromium-based browser (Chrome or Edge)

### 📦 Install Dependencies
```bash
pip install DrissionPage
```

### 🌐 Proxy Configuration
Update the `MY_PROXY` variable inside both scripts with:

```
IP:PORT
```

(Recommended: Rotating residential proxies for large-scale scraping)

---

## ▶ Usage

### 1️⃣ Run Category Harvester
```bash
python script1_harvester.py
```
Output:
```
shein_flawless.json
```

---

### 2️⃣ Run Deep Detail Scraper
```bash
python script2_deep_details.py
```
Output:
```
shein_deep_progress.json
```

---

## 📊 Final Output Structure (JSON)

Each product contains:

```json
{
  "product_name": "",
  "product_url": "",
  "price": "",
  "currency": "",
  "description": "",
  "materials": "",
  "intro_text": "",
  "image_urls": []
}
```

### Data Includes:
- ✅ Cleaned Product Titles  
- ✅ Real-Time Price & Currency Detection  
- ✅ Full Descriptions & Material Info  
- ✅ High-Resolution Image URLs  

---

## ⚠ Disclaimer

This project is intended strictly for:
- Educational purposes  
- Research  
- Data engineering practice  

Ensure compliance with SHEIN’s Terms of Service and applicable laws before deploying at scale.

---

## 📌 Key Highlights

✔ Two-Stage Scalable Architecture  
✔ CAPTCHA Recovery Logic  
✔ Smart Session Rotation  
✔ Optimized Proxy Usage  
✔ Clean Analytical JSON Output  

---

**Built for performance. Engineered for resilience.**
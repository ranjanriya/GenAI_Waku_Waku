remove redundancy:

# 📸 Manga Image Scraper (Solo Leveling)

This Python project is a web scraper built using **Scrapy** to automatically download manga chapter images from [manwha-sololeveling.com](https://www.manwha-sololeveling.com). It supports downloading multiple chapters in sequence and saves images in a structured format.

---

## 🛠 Setup Instructions

Follow these steps to set up and run the scraper:

### 1. Clone or Download the Project

```bash
git clone https://github.com/ranjanriya/GenAI_Waku_Waku.git
cd GenAI_Waku_Waku
```

### 2. Create and Activate a Virtual Environment

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install scrapy requests
```

### 4. Run the Scraper

```bash
python scraper.py
```

This will start downloading manga images from **Chapter 1 to Chapter 200** by default.

To skip running the scraper, you can download a ZIP archive of the downloaded_images/ folder directly:

👉 Click here to download images (Google Drive)

---

## 🧾 What the Code Does

1. **Spider Definition**:
   - Scrapy visits each chapter URL (e.g., `https://www.manwha-sololeveling.com/manga/solo-leveling-chapter-1/`)
   - Extracts all image URLs from the page
   - Builds chapter and page identifiers
   - Optionally downloads images using the `requests` library

2. **Image Pipeline**:
   - A custom Scrapy pipeline downloads each image using Scrapy’s downloader
   - Saves each image to `downloaded_images/` with a filename format: `chapterpage.png` (e.g., `001003.png`)

3. **Download Logic**:
   - The script can download using both:
     - `requests` (manual download)
     - Scrapy pipelines (default pipeline)
   - You can easily disable the manual method by commenting out a line in `parse()`

---

## ⚠️ Disclaimer

This scraper is for **educational purposes** only. Respect website terms of service and copyright rules.

---
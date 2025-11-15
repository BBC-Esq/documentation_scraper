# 📚 Documentation Scraper

<div align="center">

**A powerful GUI tool for downloading and archiving documentation websites for offline access**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Output](#-output)

---

</div>

## ✨ Features

- **Intuitive GUI Interface** - Easy-to-use dropdown menu for selecting documentation sources
- **Offline Access** - Download entire documentation sites for viewing without internet
- **Smart Tracking** - Visual indicators show already scraped documentation
- **Organized Storage** - Automatic folder structure with preserved formatting
- **Quick Access** - One-click folder opening to view your downloads

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/documentation-scraper.git
cd documentation-scraper
```

### 2. Set up virtual environment
```bash
python -m venv .
```

### 3. Activate the environment

**Windows:**
```bash
.\Scripts\activate
```

**Linux/macOS:**
```bash
source bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

## 💡 Usage

### Launch the application
```bash
python scraper_app.py
```

### Navigate the interface

| Action | Description |
|--------|-------------|
| **Select Documentation** | Choose from the dropdown menu |
| **Start Scraping** | Click to begin downloading |
| **Track Progress** | Already scraped docs appear in <span style="color:red">**red**</span> |
| **Open Folder** | Quick access to downloaded files |

## 📁 Output
```
Scraped_Documentation/
├── source-1/
│   ├── index.html
│   └── ...
├── source-2/
│   ├── index.html
│   └── ...
└── ...
```

✅ All documentation saved in the `Scraped_Documentation` folder  
✅ Each source gets its own organized subfolder  
✅ HTML formatting and styles preserved but surrouding irrelevant fluff is not scraped.

<div align="center">

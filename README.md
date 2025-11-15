# Documentation Scraper

A GUI-based documentation scraper that allows you to download and save documentation websites locally for offline viewing.

# Installation

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/documentation-scraper.git
   cd documentation-scraper
```

2. **Create a virtual environment**
```bash
   python -m venv .
```

3. **Activate the virtual environment**
   
```bash
   .\Scripts\activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

## Usage

1. **Run the application**
```bash
   python scraper_app.py
```

2. **Using the GUI**
   - Select documentation from the dropdown menu
   - Click "Start Scraping" to begin downloading
   - Already scraped documentation appears in red
   - Click "Open Folder" to view downloaded files

3. **Output**
   - All scraped documentation is saved in the `Scraped_Documentation` folder
   - Each documentation source gets its own subfolder
   - Files are saved as HTML with preserved formatting

# Phishing Kit Fingerprinter

A defensive security tool that collects live phishing pages from public threat feeds, extracts structural fingerprints and clusters similar kits together to identify campaign reuse across domains

## What it does
- Fetches live phishing URLs from OpenPhish
- Saves raw HTML and extracts features: page title, SHA256 hash, form actions, email addresses 
- Clusters pages into kit families using structural HTML comparison
- Stores all results in a SQLite database with timestamps

## Pipeline
get_urls.py -> fetch.py -> similarity.py -> database.py

## Tools & Libraries
- Python 3
- requests, beautifulsoup4
- sqlite3 (built-in)
- difflib (built-in)

## Usage
pip install requests beautifulsoup4
python3 get_urls.py
python3 fetch.py
python3 similarity.py
python3 database.py

## Disclaimer
This tool is built for defensive research purpose only. All URLs are sourced from public threat intelligence feeds.

## Author
**Giannis Kinalis**
*Cybersecurity Enthusiast*

- **GitHub:** [gianniskinalis](https://github.com/gianniskinalis)
- **LinkedIn:** [Ioannis Kinalis](https://linkedin.com/ioannis-kinalis)
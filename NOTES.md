Project: Phishing Kit Fingerprinter

Goal: Build a tool that collects phishing pages from public threat feeds, extracts structural fingerprints and clusters similar kits together to identify reuse patterns.

Environment Setup
- Created an isolated Ubuntu 24.04 VM in VirtualBox
- Disabled shared clipboard and drag & drop to prevent data crossing between host and VM
- Took a clean snapshot before installing any tools

Tools Installed
- Python3, pip, venv, git, curl
- VS Code with Python extension
- Python libraries: requests, beautifulsoup4

Phase 1 - Crawler
- Created project folder phish-fingerprinter with a Python virual environment
- Wrote fetch.py: fetches a URL with a spoofed User-Agent header, handles SSL errors, saves raw HTML to disk
- Extended the script to read from urls.txt and save each page to a data/ folder with a sanitized filename
- Tested against example.com, example.org, example.net and all returned 200 with correct HTML saved

Phase 2 - Feature Extractor
- Wrote extractor.py: opens each saved HTML file and extracts page title, SHA256 hash of raw content, form action URLs and email addresses using regex
- Tested against saved example pages and confirmed identical SHA256 across example.com and example.org, proving the hash fingeprinting works correctly
- No forms or emails found as expected, example.com is a plain static page

Phase 3 - Live Threat Data
- Switched from PhishTank to OpenPhish free feed (PhishTank registration temporarily disabled)
- Wrote get_urls.py: pulls 10 live verified phishing URLs from OpenPhish and saves to urls.txt
- Ran full pipeline: get_urls.py -> fetch.py -> extractor.py
- Successfully extracted real phishing page data and identified fake Shopee and fake Steam pages
- Observed first real fingerprints: page titles, SHA256 hashes, form structures

Phase 4 - Similarity Engine
- Wrote similarity.py: groups pages into kit families using SHA256 hash matching and structural HTML tag sequence comparison via SequenceMatcher, compares lightweight tag skeletons instead of raw HTML for performance
- Optimized comparison by extracting tag structure instead of raw HTML to handle large files
- First real results: detected two seperate Shopee phishing domains sharing the same kit structure and confirmed campaign reuse across domains
- Identified 4 distinct kit families: Apple iCloud, Shopee, Netflix, and a SHopee variant
- Known issue: duplicate page assignment in clustering, to fix in next version

Phase 5 - Database
- Wrote database.py: initializes a SQLite database, stores extracted features permanently with timestamp
- Connected similarity.py to the database, results now saved automatically after clustering
- Added duplicate detection using SHA256, same page won't be inserted twice
- Final database contains 5 pages across 4 kit families, with family_3 correctly grouping two Shopee domains together
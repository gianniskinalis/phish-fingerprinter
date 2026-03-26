import os
import hashlib
import re
from bs4 import BeautifulSoup

data_folder = "data"

def extract_features(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Page title
    title = soup.title.string.strip() if soup.title else "No title"

    # SHA256 hash of raw html
    sha256 = hashlib.sha256(html.encode()).hexdigest()

    # Form action URLs
    forms = [form.get("ation", "No action") for form in soup.find_all("form")]

    # Email addresses
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\[a-zA-Z]{2,}", html)

    return {
        "file": filepath,
        "title": title,
        "sha256": sha256,
        "forms": forms,
        "emails": emails
    }   

for filename in os.listdir(data_folder):
    if filename.endswith(".html"):
        filepath = os.path.join(data_folder, filename)
        features = extract_features(filepath)

        print(f"\n[FILE] {features['file']}")
        print(f"  Title:  {features['title']}")
        print(f"  SHA256:  {features['sha256']}")
        print(f"  Forms:  {features['forms']}")
        print(f"  Emails:  {features['emails']}")
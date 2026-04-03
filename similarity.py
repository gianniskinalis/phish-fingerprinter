import os
import hashlib
import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from database import init_db, save_page

data_folder = "data"


def get_structure(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = [tag.name for tag in soup.find_all()]
    return " ".join(tags)


def similarity(a, b):
    return round(SequenceMatcher(None, a, b).ratio(), 2)


def extract_features(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title else "No title"
    sha256 = hashlib.sha256(html.encode()).hexdigest()
    forms = [form.get("action", "No action") for form in soup.find_all("form")]
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)

    return {
        "file": filepath,
        "title": title,
        "sha256": sha256,
        "forms": forms,
        "emails": emails,
        "html": html,
        "structure": get_structure(html)
    }


pages = []
for filename in os.listdir(data_folder):
    if filename.endswith(".html"):
        filepath = os.path.join(data_folder, filename)
        pages.append(extract_features(filepath))

print(f"[+] Loaded {len(pages)} pages\n")

clusters = []
assigned = set()

for i, page in enumerate(pages):
    if i in assigned:
        continue

    cluster = [page]
    assigned.add(i)

    for j, other in enumerate(pages):
        if j in assigned:
            continue

        if page["sha256"] == other["sha256"]:
            cluster.append(other)
            assigned.add(i)
            continue

        score = similarity(page["structure"], other["structure"])
        if score >= 0.85:
            cluster.append(other)
            assigned.add(i)

    clusters.append(cluster)

print(f"[+] Found {len(clusters)} kit families\n")

init_db()

for i, cluster in enumerate(clusters):
    kit_family = f"family_{i+1}"
    print(f"--- Kit family {i+1} ({len(cluster)} page(s)) ---")
    for page in cluster:
        print(f"  File:  {page['file']}")
        print(f"  Title:  {page['title']}")
        print(f"  SHA256:  {page['sha256']}")
        print(f"  Forms:  {page['forms']}")
        print(f"  Emails:  {page['emails']}")
        save_page(
            url=page['file'],
            title=page['title'],
            sha256=page['sha256'],
            forms=page['forms'],
            emails=page['emails'],
            kit_family=kit_family
        )
    print()

print("[+] Results saved to database")

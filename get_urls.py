import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_phishing_urls(limit=5):
    url = "https://openphish.com/feed.txt"

    response = requests.get(url, verify=False, timeout=10)

    urls = response.text.strip().split("\n")[:limit]

    with open("urls.txt", "w") as f:
        for u in urls:
            f.write(u + "\n")

    print(f"[+] Saved {len(urls)} phishing URLs to urls.txt")
    for u in urls:
        print(f"  {u}")

get_phishing_urls()
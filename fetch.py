import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://example.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

os.makedirs("data", exist_ok=True)

with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)

        filename = url.replace("https://", "").replace("/", "_")
        filepath = f"data/{filename}.html"

        with open(filepath, "w") as f:
            f.write(response.text)

        print(f"[+] {url} - {response.status_code} - "
	      f"{len(response.text)} chars - saved to {filepath}")

    except Exception as e:
        print(f"[-] {url} - Error: {e}")

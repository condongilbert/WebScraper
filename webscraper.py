import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



# URL to scrape
url = "https://www.berkshirehathaway.com/news/2024news.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Directory to save files
pdf_dir = "berkshire_pdfs"
os.makedirs(pdf_dir, exist_ok=True)

# File to store previously downloaded links
downloaded_links_file = os.path.join(pdf_dir, "downloaded_links.txt")

# Load previously downloaded links (if any)
if os.path.exists(downloaded_links_file):
    with open(downloaded_links_file, "r") as file:
        downloaded_links = set(file.read().splitlines())
else:
    downloaded_links = set()

# Get HTML content from the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links on the page
new_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    full_link = urljoin(url, href)  # Form the full URL for each link

    # Filter to check if this link has already been downloaded
    if full_link not in downloaded_links:
        new_links.append(full_link)
        print(f"Found new link: {full_link}")  # Debug: Print each new link

# Check if there are any new links to download
if not new_links:
    print("No new links found to download.")
else:
    # Download each new link
    for link_url in new_links:
        filename = link_url.split("/")[-1]
        file_path = os.path.join(pdf_dir, filename)

        print(f"Downloading {filename} from {link_url}...")
        try:
            file_content = requests.get(link_url).content
            with open(file_path, "wb") as file:
                file.write(file_content)

            # Add to downloaded links set
            downloaded_links.add(link_url)
        except Exception as e:
            print(f"Failed to download {link_url}: {e}")

    # Update the downloaded links file
    with open(downloaded_links_file, "w") as file:
        file.write("\n".join(downloaded_links))

    print("Download complete. New files have been saved.")
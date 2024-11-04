import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL to scrape
url = "https://www.berkshirehathaway.com/news/2024news.html"

# Directory to save PDFs
pdf_dir = "berkshire_pdfs"
os.makedirs(pdf_dir, exist_ok=True)

# File to store previously downloaded PDF links
downloaded_pdfs_file = os.path.join(pdf_dir, "downloaded_pdfs.txt")

# Load previously downloaded PDFs (if any)
if os.path.exists(downloaded_pdfs_file):
    with open(downloaded_pdfs_file, "r") as file:
        downloaded_pdfs = set(file.read().splitlines())
else:
    downloaded_pdfs = set()

# Get HTML content from the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find and display all links to verify if PDFs are being found correctly
pdf_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    # Use urljoin to handle both relative and absolute URLs
    full_link = urljoin(url, href)
    if full_link.endswith('.pdf'):
        pdf_links.append(full_link)
        print(f"Found PDF link: {full_link}")  # Debug: Print each PDF link

# Filter out only the new PDF links
new_pdfs = [pdf for pdf in pdf_links if pdf not in downloaded_pdfs]

# Check if there are any new PDFs to download
if not new_pdfs:
    print("No new PDFs found to download.")
else:
    # Download new PDFs
    for pdf_url in new_pdfs:
        pdf_name = pdf_url.split("/")[-1]
        pdf_path = os.path.join(pdf_dir, pdf_name)

        print(f"Downloading {pdf_name}...")
        pdf_content = requests.get(pdf_url).content
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_content)
        
        # Add to downloaded PDFs set
        downloaded_pdfs.add(pdf_url)

    # Update the downloaded PDFs file
    with open(downloaded_pdfs_file, "w") as file:
        file.write("\n".join(downloaded_pdfs))

    print("Download complete. New PDFs have been saved.")
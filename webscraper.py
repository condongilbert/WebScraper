from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import time
import PyPDF2

# Path to ChromeDriver
driver_path = "C:/Users/v-gcondon/Downloads/chromedriver-win64/chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode, optional
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create a Service object
service = Service(driver_path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the URL
    url = "https://www.berkshirehathaway.com/news/2024news.html"
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load content

    # Extract only PDF links
    link_elements = driver.find_elements("tag name", "a")
    pdf_links = [element.get_attribute("href") for element in link_elements if element.get_attribute("href") and element.get_attribute("href").endswith(".pdf")]
    
    # Select the first (most recent) PDF link
    recent_pdf_url = pdf_links[0]
    
    # Download the PDF
    response = requests.get(recent_pdf_url)
    pdf_path = "recent_report.pdf"
    with open(pdf_path, "wb") as file:
        file.write(response.content)
    print(f"Downloaded {pdf_path}.")

finally:
    driver.quit()

# Analysis of the downloaded PDF
def analyze_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Example analysis: Extract financial keywords
    keywords = ["net earnings", "shareholders", "investment", "insurance", "float"]
    for keyword in keywords:
        occurrences = text.lower().count(keyword)
        print(f"{keyword.capitalize()} mentioned {occurrences} times.")

# Perform the PDF analysis
analyze_pdf(pdf_path)
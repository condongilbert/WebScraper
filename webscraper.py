from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

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
    
    # Save PDF links to a text file
    with open("pdf_links.txt", "w", encoding="utf-8") as file:
        for link in pdf_links:
            file.write(link + "\n")
    print("PDF links extracted and saved as 'pdf_links.txt'.")

finally:
    driver.quit()